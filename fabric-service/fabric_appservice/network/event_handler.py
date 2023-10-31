import os
import json
import copy

from bson.objectid import ObjectId

from settings import config
from utils.logging import get_logger
import const
from celery_worker.tasks import (
    deploy_fabric,
    update_network,
    generate_new_remote_peer,
    delete_network_folder,
    delete_dapp_gitlab,
)
from utils import schemas, get_folder_path
import k8s.digitalocean as k8s
from exceptions import ThirdPartyRequestError, ServiceError, NotSupported, SchemaError
from account import account_handler
from storage import storage_handler
from jsonschema import validate, ValidationError, FormatChecker
from network import update_network_config
from network.error import NetworkCreateErrorStatus

_LOGGER = get_logger(__name__)


class NetworkHandler:
    def __init__(self, database, broker_client):
        self.__database = database
        self.__broker_client = broker_client

    async def handle_create_network(self, body, reply_to, message_id):
        try:
            new_network = body["network_info"]
            user_info = body["user_info"]

            await self.__database.create_network(
                {
                    "_id": ObjectId(new_network["network_id"]),
                    "user_id": user_info["user_id"],
                }
            )

            validate(instance=new_network, schema=schemas.network_config_schema)
            _LOGGER.debug(
                f"Receive a request to create a network with network_id: {new_network['network_id']}"
            )

            modification = {
                "name": new_network["name"],
                "node_infrastructure": new_network["node_infrastructure"],
                "blockchain_peer_config": new_network["blockchain_peer_config"],
            }

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=new_network["network_id"],
                modification=modification,
            )

            token = account_handler.get_token()

            user_folder = storage_handler.get_user_folder(token)

            network_folder_id = storage_handler.create_folder(
                token,
                {
                    "name": new_network["name"],
                    "parent_id": user_folder["folder_id"],
                    "shared": [user_info["user_id"]],
                },
            )

            modification = {
                "network_folder_id": network_folder_id,
            }

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=new_network["network_id"],
                modification=modification,
            )

            cluster_id = k8s.create_cluster(
                name="fabric" + new_network["network_id"],
                cpu=new_network["node_infrastructure"]["node_plan"]["cpu"],
                ram=new_network["node_infrastructure"]["node_plan"]["ram"],
                number_nodes=new_network["node_infrastructure"]["number_vm_nodes"],
                digital_ocean_token=config["k8s"]["token"],
            )
            # cluster_id = "68b11e3c-7389-4940-b47b-04a763510a8a"

            network_folder = get_folder_path.get_network_folder_path(
                username=user_info["username"], network_id=new_network["network_id"]
            )

            modification = {
                "cluster_id": cluster_id,
            }

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=new_network["network_id"],
                modification=modification,
            )

            # if not os.path.exists(network_folder):
            #     _LOGGER.debug(f"Create folder: {network_folder}")
            #     os.makedirs(network_folder)

            deploy_fabric.delay(
                generated_folder=network_folder,
                cluster_id=cluster_id,
                network_info=new_network,
                user_info=user_info,
                reply_to=reply_to,
            )

        except (ThirdPartyRequestError, SchemaError) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": new_network["network_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Fail create network with network_id: {new_network['network_id']} due to {e.message}"
            )

        except ValidationError as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": new_network["network_id"],
                    "message": f"Schema Error: {e.message} on {e.relative_schema_path}",
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Fail create network with network_id: {new_network['network_id']} due to {e.message}"
            )

    async def handle_delete_network(self, body, reply_to, message_id):
        network_info = body["network_info"]
        user_info = body["user_info"]
        list_dapps = body["dapps"]
        deleted_dapps = []
        _LOGGER.debug(
            f"Receive a request to delete a network with network_id {network_info['network_id']}"
        )

        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "network_id": network_info["network_id"],
            }
        }
        await self.__broker_client.publish(
            routing_key=reply_to, message=json.dumps(success_message)
        )

        networks = await self.__database.get_networks(
            network_id=network_info["network_id"]
        )
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {network_info['network_id']}"
            )

        elif len(networks) == 0:
            raise ServiceError(
                f"Don't have network with network_id: {network_info['network_id']}"
            )

        network = networks[0]
        network["network_id"] = network_info["network_id"]

        # cluster_id = network["cluster_id"]
        try:
            if "cluster_id" in network and network["cluster_id"]:
                k8s.delete_cluster(
                    cluster_id=network["cluster_id"],
                    digital_ocean_token=config["k8s"]["token"],
                )

                modification = {"cluster_id": None}

                await self.__database.update_network(
                    user_id=user_info["user_id"],
                    network_id=network_info["network_id"],
                    modification=modification,
                )

            dapps = await self.__database.get_dapps(
                network_id=network_info["network_id"], user_id=user_info["user_id"]
            )

            for dapp in dapps:
                deleted_dapps.append(dapp["dapp_id"])
                delete_dapp_gitlab.delay(dapp["dapp_id"])

            await self.__database.delete_dapp(network_id=network_info["network_id"])

            if "network_folder_id" in network and network["network_folder_id"]:

                token = account_handler.get_token()

                storage_handler.delete_folder(token, network["network_folder_id"])

                modification = {"network_folder_id": None}

                await self.__database.update_network(
                    user_id=user_info["user_id"],
                    network_id=network_info["network_id"],
                    modification=modification,
                )

            await self.__database.delete_network(network_id=network_info["network_id"])

            delete_network_folder.delay(network_info=network_info, user_info=user_info)

        except ThirdPartyRequestError as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network_info["network_id"],
                    "deleted_dapps": deleted_dapps,
                    "list_dapps": list_dapps,
                    "message": e.message,
                }
            }
            # await self.__broker_client.publish(
            #     routing_key=reply_to, message=json.dumps(failure_message)
            # )
            _LOGGER.debug(
                f"Fail to delete network with network_id: {network_info['network_id']}"
            )

    async def handle_retry_create_network(self, body, reply_to, message_id):
        network_info = body["network_info"]
        user_info = body["user_info"]
        _LOGGER.debug(
            f"Receive a request to retry creating network with network_id {network_info['network_id']}"
        )

        networks = await self.__database.get_networks(
            network_id=network_info["network_id"]
        )
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {network_info['network_id']}"
            )
        elif len(networks) == 0:
            raise NotSupported(
                f"Don't have network with network_id: {network_info['network_id']}"
            )

        network = networks[0]

        # network["network_id"] = network_info["network_id"]

        try:
            validate(instance=network, schema=schemas.network_config_schema)
            if "cluster_id" in network and network["cluster_id"]:
                cluster_id = network["cluster_id"]

                k8s.delete_cluster(
                    cluster_id=cluster_id,
                    digital_ocean_token=config["k8s"]["token"],
                )

            cluster_id = k8s.create_cluster(
                name="fabric" + network["network_id"],
                cpu=network["node_infrastructure"]["node_plan"]["cpu"],
                ram=network["node_infrastructure"]["node_plan"]["ram"],
                number_nodes=network["node_infrastructure"]["number_vm_nodes"],
                digital_ocean_token=config["k8s"]["token"],
            )

            modification = {
                "cluster_id": cluster_id,
            }

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=network_info["network_id"],
                modification=modification,
            )

            if "network_folder_id" not in network or not network["network_folder_id"]:

                token = account_handler.get_token()

                user_folder = storage_handler.get_user_folder(token)

                network_folder_id = storage_handler.create_folder(
                    token,
                    {
                        "name": network["name"],
                        "parent_id": user_folder["folder_id"],
                        "shared": [user_info["user_id"]],
                    },
                )

                modification = {"network_folder_id": network_folder_id}

                await self.__database.update_network(
                    user_id=user_info["user_id"],
                    network_id=network_info["network_id"],
                    modification=modification,
                )

            network_folder = get_folder_path.get_network_folder_path(
                username=user_info["username"], network_id=network["network_id"]
            )

            deploy_fabric.delay(
                generated_folder=network_folder,
                cluster_id=cluster_id,
                network_info=network,
                user_info=user_info,
                reply_to=reply_to,
            )

        except (ThirdPartyRequestError, NotSupported) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network["network_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Fail to retry creating network with network_id: {network['network_id']}"
            )

    async def handle_update_network(self, body, reply_to, message_id):

        network_id = body["network_id"]
        user_info = body["user_info"]
        update_info = body["update_info"]

        _LOGGER.debug(
            f"Receive a request to update network with network_id {network_id}"
        )
        try:
            networks = await self.__database.get_networks(network_id=network_id)
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {network_id}"
                )
            elif len(networks) == 0:
                raise NotSupported(f"Don't have network with network_id: {network_id}")

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=network_id,
                modification={"latest_update": update_info},
            )

            network = networks[0]
            network["network_id"] = network_id

            dapps = await self.__database.get_dapps(
                network_id=network_id, user_id=user_info["user_id"]
            )
            validate(instance=update_info, schema=schemas.network_update_info_schema)

            new_network_config = update_network_config.update_network_config(
                network, update_info
            )
            modification = copy.deepcopy(new_network_config)

            modification.pop("network_id", None)
            modification.pop("latest_update", None)
            modification.pop("error", None)

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=network_id,
                modification=modification,
            )

            update_network.delay(
                old_network_config=network,
                new_network_config=new_network_config,
                update_type=update_info["update_type"],
                dapps=dapps,
                user_info=user_info,
                reply_to=reply_to,
            )

        except (ThirdPartyRequestError, NotSupported, SchemaError) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network["network_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to update network with network_id: {network_id}")
        except ValidationError as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network_id,
                    "message": f"Schema Error: {e.message} on {e.relative_schema_path}",
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail update network with network_id: {network_id}")

    async def handle_retry_update_network(self, body, reply_to, message_id):

        network_id = body["network_id"]
        user_info = body["user_info"]

        _LOGGER.debug(
            f"Receive a request to retry update network with network_id {network_id}"
        )

        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {network_id}"
            )
        elif len(networks) == 0:
            raise NotSupported(f"Don't have network with network_id: {network_id}")

        try:
            network = networks[0]
            network["network_id"] = network_id

            if "error" not in network:
                raise NotSupported(f"No Error found yet")

            if not network["error"]:
                raise NotSupported(f"No Error found yet")

            if "latest_update" not in network:
                raise NotSupported(f"No Update found yet")

            if not network["latest_update"]:
                raise NotSupported(f"No Update found yet")

            dapps = await self.__database.get_dapps(
                network_id=network_id, user_id=user_info["user_id"]
            )

            validate(
                instance=network["latest_update"],
                schema=schemas.network_update_info_schema,
            )

            new_network_config = update_network_config.update_network_config(
                network, network["latest_update"]
            )
            modification = copy.deepcopy(new_network_config)

            modification["error"] = None

            modification.pop("network_id", None)

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=network_id,
                modification=modification,
            )

            update_network.delay(
                old_network_config=network,
                new_network_config=new_network_config,
                update_type=network["latest_update"]["update_type"],
                dapps=dapps,
                user_info=user_info,
                reply_to=reply_to,
            )

        except (ThirdPartyRequestError, NotSupported, SchemaError) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network["network_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to update network with network_id: {network_id}")
        except ValidationError as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network_id,
                    "message": f"Schema Error: {e.message} on {e.relative_schema_path}",
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail update network with network_id: {network_id}")

    async def handle_rollback_update_network(self, body, reply_to, message_id):

        network_id = body["network_id"]
        user_info = body["user_info"]

        _LOGGER.debug(
            f"Receive a request to rollback network with network_id {network_id}"
        )

        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {network_id}"
            )
        elif len(networks) == 0:
            raise NotSupported(f"Don't have network with network_id: {network_id}")

        try:
            network = networks[0]
            network["network_id"] = network_id

            if "latest_update" not in network:
                raise NotSupported(f"No Update found yet")

            if not network["latest_update"]:
                raise NotSupported(f"No Update found yet")

            modification = {"error": None, "latest_update": None}

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=network_id,
                modification=modification,
            )

            success_message = {
                "data": {
                    "user_id": user_info["user_id"],
                    "network_id": network["network_id"],
                    "new_network_config": {},
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(success_message)
            )

        except (ThirdPartyRequestError, NotSupported, SchemaError) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network["network_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to update network with network_id: {network_id}")
        except ValidationError as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network_id,
                    "message": f"Schema Error: {e.message} on {e.relative_schema_path}",
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail update network with network_id: {network_id}")

    async def handle_network_error(self, body, reply_to, message_id):
        network_info = body["network_info"]
        user_info = body["user_info"]
        _LOGGER.debug(f"Receive message about network error")

        modification = copy.deepcopy(network_info)

        modification.pop("network_id", None)
        modification.pop("latest_update", None)

        await self.__database.update_network(
            user_id=user_info["user_id"],
            network_id=network_info["network_id"],
            modification=modification,
        )

    async def handle_create_resource(self, body, reply_to, message_id):
        try:
            network_id = body["network_id"]
            resource_info = body["resource_info"]
            user_info = body["user_info"]

            validate(
                instance=resource_info,
                schema=schemas.resource_config_schema,
                format_checker=FormatChecker(),
            )

            _LOGGER.debug(
                f"Receive a request to create new resouce for network with network_id {network_id}"
            )

            networks = await self.__database.get_networks(network_id=network_id)

            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {network_id}"
                )
            elif len(networks) == 0:
                raise ServiceError(f"Don't have network with network_id: {network_id}")

            network = networks[0]
            network["network_id"] = network_id

            old_peer_config = network["blockchain_peer_config"]

            new_peer_config = copy.deepcopy(old_peer_config)

            org_index = 0

            for org in old_peer_config["organizations"]:
                if (
                    org["name"].lower()
                    == resource_info["resource_config"]["organization_name"].lower()
                ):
                    break
                else:
                    org_index += 1

            if org_index >= len(network["blockchain_peer_config"]["organizations"]):
                raise NotSupported("Organization name does not exist")

            if "remote_peers" not in new_peer_config["organizations"][org_index]:
                new_peer_config["organizations"][org_index]["remote_peers"] = []

            peer_index = new_peer_config["organizations"][org_index][
                "number_peer"
            ] + len(new_peer_config["organizations"][org_index]["remote_peers"])

            new_peer_config["organizations"][org_index]["remote_peers"].append(
                {
                    "host": resource_info["resource_config"]["host"],
                    "port": resource_info["resource_config"]["port"],
                }
            )

            resources_folder_id = (
                network["resources_folder_id"]
                if "resources_folder_id" in network
                else None
            )

            token = account_handler.get_token()

            if not resources_folder_id:
                resources_folder_id = storage_handler.create_folder(
                    token,
                    {
                        "name": "resources",
                        "parent_id": network["network_folder_id"],
                        "shared": [user_info["user_id"]],
                    },
                )

            await self.__database.update_network(
                user_id=user_info["user_id"],
                network_id=network_id,
                modification={
                    "blockchain_peer_config": new_peer_config,
                    "resources_folder_id": resources_folder_id,
                },
            )

            generate_new_remote_peer.delay(
                network_config=network,
                resource_info=resource_info,
                user_info=user_info,
                resources_folder_id=resources_folder_id,
                token=token,
                org_index=org_index,
                peer_index=peer_index,
                host=resource_info["resource_config"]["host"],
                port=resource_info["resource_config"]["port"],
                reply_to=reply_to,
            )

        except (ThirdPartyRequestError, NotSupported) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "resource_id": resource_info["resource_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Fail create resource with resouce_id {resource_info['resource_id']} for network with network_id: {network_id}"
            )

        except ValidationError as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "resource_id": resource_info["resource_id"],
                    "message": f"Schema Error: {e.message} on {e.relative_schema_path}",
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Fail create resource with resouce_id {resource_info['resource_id']} for network with network_id: {network_id}"
            )
