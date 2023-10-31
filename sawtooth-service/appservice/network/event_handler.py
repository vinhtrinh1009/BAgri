from distutils.config import DEFAULT_PYPIRC
import os
import json
import shutil
import jwt

from bson.objectid import ObjectId

from config.logging_config import get_logger
from generator import sawtooth_generator
from worker.tasks import (
    deploy_sawtooth,
    task_delete_folder_network,
    task_upload_resources,
)
from includes import k8s
from settings import config
from exceptions import GitlabError, OperationError, ThirdPartyRequestError, ServiceError, NotSupported
from constants import BASE_DIR
from includes.account_handler import get_token, get_user_info, update_user_info
from includes.storage_handler import *
import includes.git_handler as git_handle
from includes.resource_handler import gen_resource
from operation import k8s_operation
from jsonschema import validate, ValidationError, FormatChecker

import schemas

_LOGGER = get_logger(__name__)


class NetworkHandler:
    def __init__(self, database, broker_client):
        self.__database = database
        self.__broker_client = broker_client

    async def handle_create_network(self, body, reply_to, message_id):
        network_info = body["network_info"]
        user_info = body["user_info"]
        _LOGGER.debug(
            f"Receive a request to create a network with network_id: {network_info['network_id']}"
        )
        try:
            validate(instance=network_info, schema=schemas.network_config_schema)
            
            await self.__database.create_network(
                {
                    "_id": ObjectId(network_info["network_id"]),
                }
            )

            cluster_id = k8s.create_cluster(
                name=f'sawtooth{network_info["network_id"]}',
                cpu=network_info["node_infrastructure"]["node_plan"]["cpu"],
                ram=network_info["node_infrastructure"]["node_plan"]["ram"],
                number_nodes=network_info["node_infrastructure"]["number_vm_nodes"],
                digital_ocean_token=config["k8s"]["token"],
            )

            modification = {
                "cluster_id": cluster_id,
                "name": network_info["name"],
                "number_peer": network_info["blockchain_peer_config"]["number_peer"],
                "node_infrastructure": network_info["node_infrastructure"],
                "blockchain_peer_config": network_info["blockchain_peer_config"],
                "consensus": network_info["consensus"],
            }

            await self.__database.update_network(
                network_id=network_info["network_id"], modification=modification
            )

            _LOGGER.debug(f"token: {get_token()}")

            token = get_token()["data"]["token"]

            user_folder = get_user_folder(token)

            network_folder_id = create_folder(
                token,
                {
                    "name": network_info["name"],
                    "parent_id": user_folder["folder_id"],
                    "shared": [user_info["user_id"]],
                },
            )

            await self.__database.update_network(
                network_id=network_info["network_id"],
                modification={"network_folder_id": network_folder_id},
            )

            resources_folder_id = create_folder(
                token,
                {
                    "shared": [user_info["user_id"]],
                    "name": "resources",
                    "parent_id": network_folder_id,
                },
            )

            await self.__database.update_network(
                network_id=network_info["network_id"],
                modification={
                    "resources_folder_id": resources_folder_id,
                },
            )

            deploy_sawtooth.apply_async(
                args=[cluster_id, network_info, user_info, reply_to],
                queue="sawtooth.tasks",
            )

        except (ThirdPartyRequestError, ValidationError, StorageServiceRequestError) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network_info["network_id"],
                    "message": e.message,
                }
            }
            _LOGGER.debug(failure_message)
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Failed to create network with network_id: {network_info['network_id']}"
            )

    async def handle_delete_network(self, body, reply_to, message_id):
        network_info = body["network_info"]
        user_info = body["user_info"]
        dapp_infos = body["dapps"]
        deleted_dapps = []
        _LOGGER.debug(
            f"Receive a request to delete a network with network_id {network_info['network_id']}"
        )
        networks = await self.__database.get_networks(
            network_id=network_info["network_id"]
        )
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {network_info['network_id']}"
            )
        elif len(networks) == 0:
            success_message = {
                "data": {
                    "user_id": user_info["user_id"],
                    "network_id": network_info["network_id"],
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(success_message)
            )
            _LOGGER.debug(
                f"Deleted network with network_id: {network_info['network_id']}"
            )
            return

        network = networks[0]
        token = get_token()["data"]["token"]

        try:
            if "cluster_id" in network:
                k8s.delete_cluster(
                    cluster_id=network["cluster_id"],
                    digital_ocean_token=config["k8s"]["token"],
                )
            await self.__database.delete_network(network_id=network_info["network_id"])

            # os.system("rm -rf " + os.path.join(BASE_DIR,
            #                                    "network/{}/{}/".format(user_info['username'],
            #                                                         network_info['network_id'])))
            
            resources = await self.__database.get_resources(
                network_id=network_info["network_id"]
            )

            for dapp_info in dapp_infos:
                dapp_info["dapp_name"] = "{}-{}".format(
                    dapp_info["dapp_name"], str(dapp_info["dapp_id"][-5:])
                )
                user_groups = git_handle.get_groups(
                    user_info["username"], config["gitlab"]["dapp_group_id"]
                )
                if len(user_groups) == 1:
                    user_group_id = user_groups[0]["id"]
                    dapp_groups = git_handle.get_groups(
                        dapp_info["dapp_name"], user_group_id
                    )
                    if len(dapp_groups) == 1:
                        dapp_group_id = dapp_groups[0]["id"]
                        git_handle.delete_group(dapp_group_id)

                await self.__database.delete_dapp(
                    dapp_id=dapp_info["dapp_id"], user_id=user_info["user_id"]
                )

                dapp_code_folder = os.path.join(
                    BASE_DIR,
                    "application/{0}/{1}".format(
                        user_info["username"], dapp_info["dapp_name"]
                    ),
                )

                # os.system("rm -rf " + dapp_code_folder)
                if os.path.exists(dapp_code_folder):
                    shutil.rmtree(dapp_code_folder)
                deleted_dapps.append(dapp_info)
            for resource in resources:
                await self.__database.delete_resource(
                    resource_id=resource["resource_id"], user_id=user_info["user_id"]
                )
            vchain_ingress_path = os.path.join(
                BASE_DIR,
                "network/{0}/{1}/explorer_vchain_ingress.yaml".format(
                        user_info["username"], network_info["network_id"]
                ),
            )
            vchain_pod_config_path = os.path.join(
                BASE_DIR,
                "k8s",
                "v-chain-prod-kubeconfig.yaml",
            )
            if os.path.exists(vchain_ingress_path):
                k8s_operation.delete(vchain_ingress_path,vchain_pod_config_path)

            network_folder = os.path.join(
                BASE_DIR,
                "network/{0}/{1}".format(
                    user_info["username"], network_info["network_id"]
                ),
            )
            if os.path.exists(network_folder):
                shutil.rmtree(network_folder)

            volume_folder = os.path.join(
                BASE_DIR,
                "volume/{0}/{1}".format(
                    user_info["username"], network_info["network_id"]
                ),
            )
            if os.path.exists(volume_folder):
                shutil.rmtree(volume_folder)   
 
            if "network_folder_id" in network:
                task_delete_folder_network.delay(
                    token,
                    network["network_folder_id"],
                    user_info,
                    network_info,
                    deleted_dapps,
                    dapp_infos,
                    reply_to,
                )
            else:
                success_message = {
                    "data": {
                        "user_id": user_info["user_id"],
                        "network_id": network_info["network_id"],
                    }
                }
                await self.__broker_client.publish(
                    routing_key=reply_to, message=json.dumps(success_message)
                )
            _LOGGER.debug(
                f"Deleted network with network_id: {network_info['network_id']}"
            )
        except (ThirdPartyRequestError, OperationError) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": network_info["network_id"],
                    "message": e.message,
                    "list_dapps": dapp_infos,
                    "deleted_dapps": deleted_dapps
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Fail to delete network with network_id: {network_info['network_id']}"
            )

    async def handle_create_resource(self, body, reply_to, message_id):
        try:
            resource_info = body["resource_info"]
            user_info = body["user_info"]
            network_id = body["network_id"]
            _LOGGER.debug(
                f"Receive a request to create a resource with resource info: {resource_info}"
            )

            validate(instance=resource_info, schema=schemas.resource_config_schema)

            networks = await self.__database.get_networks(network_id=network_id)
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {network_id}"
                )
            elif len(networks) == 0:
                raise ServiceError(f"Don't have network with network_id: {network_id}")

            # Get network info
            network = networks[0]
            network_folder_id = network["network_folder_id"]
            public_ip = k8s.get_public_ip(
                cluster_id=network["cluster_id"],
                digital_ocean_token=config["k8s"]["token"],
            )

            # Get list dapp
            dapps = await self.__database.get_dapps(network_id=network_id)

            # Get deploy token
            users = await self.__database.get_users(user_id=user_info["user_id"])
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one user with user_id: {user_info['user_id']}"
                )
            elif len(networks) == 0:
                raise ServiceError(
                    f"Don't have user with user_id: {user_info['user_id']}"
                )
            if len(users) == 0:
                user_groups = git_handle.get_groups(
                    user_info["username"], config["gitlab"]["dapp_group_id"]
                )

                if len(user_groups) == 1:
                    user_group_id = user_groups[0]["id"]
                elif len(user_groups) == 0:
                    user_group_id = git_handle.create_group(
                        user_info["username"], config["gitlab"]["dapp_group_id"]
                    )
                
                deploy_token = git_handle.gen_deploy_token(user_group_id)
                encrypt_token = jwt.encode(
                    deploy_token,
                    key=config["jwt_key"],
                    algorithm="HS256",
                )
                await self.__database.create_user(
                    {
                        "_id": ObjectId(user_info["user_id"]),
                        "user_name": user_info["username"],
                        "deploy_token": encrypt_token,
                    }
                )
                user_info["deploy_token"] = deploy_token
            else:
                user = users[0]
                deploy_token = jwt.decode(
                    user["deploy_token"], config["jwt_key"], algorithms=["HS256"]
                )
                user_info["deploy_token"] = deploy_token

            # Get token
            token = get_token()["data"]["token"]
            _LOGGER.debug({token})

            resource_folder_path = f"network/{user_info['username']}/{network_id}"

            resources_folder = os.path.join(
                BASE_DIR, "{0}/resources/".format(resource_folder_path)
            )
            if not os.path.exists(resources_folder):
                os.makedirs(resources_folder)

            dst_folder = f"network/{user_info['username']}/{network_id}/resources"

            # Create new record on mongo
            await self.__database.create_resource(
                {
                    "resource_id": ObjectId(resource_info["resource_id"]),
                    "user_id": user_info["user_id"],
                    "network_id": network_id,
                    "resource_config": resource_info["resource_config"],
                }
            )

            resource_info["consensus"] = network["consensus"]
            resources_folder_id = network["resources_folder_id"]

            await gen_resource(
                resource_info=resource_info,
                user_info=user_info,
                number_peer=network["number_peer"],
                public_ip=public_ip,
                dapps=dapps,
                dst_folder=dst_folder,
            )

            resources_path = os.path.join(
                BASE_DIR, f"network/{user_info['username']}/{network_id}/resources/{resource_info['resource_name']}"
            )

            resource_folder_id = create_folder(
                token,
                {
                    "shared": [user_info["user_id"]],
                    "name": "resources",
                    "parent_id": resources_folder_id,
                },
            )

            task_upload_resources.delay(
                token,
                user_info,
                resource_folder_id,
                resources_path,
                resource_info,
                reply_to,
            )

            _LOGGER.debug(
                f"Successfully create the resource with resource_id: {resource_info['resource_id']}"
            )

        except (ServiceError, ThirdPartyRequestError, ValidationError, GitlabError) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "resource_id": resource_info["resource_id"],
                    "message": e.message,
                }
            }
            _LOGGER.debug(failure_message)
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Fail create the resource with resource_id: {resource_info['resource_id']}"
            )

    async def handle_retry_create_network(self, body, reply_to, message_id):
        try:
            network_info = body["network_info"]
            _LOGGER.debug(network_info)
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
                raise ServiceError(
                    f"Don't have network with network_id: {network_info['network_id']}"
                )

            network = networks[0]
            network["network_id"] = network_info["network_id"]

            if not "error" in network:
                raise ServiceError(
                    f"The network with network_id {network['network_id']} created sucessfully already"
                )

            if not network["error"]:
                raise NotSupported(
                    f"The network with network_id {network['network_id']} created sucessfully already"
                )

            if "cluster_id" in network:
                k8s.delete_cluster(
                    cluster_id=network["cluster_id"],
                    digital_ocean_token=config["k8s"]["token"],
                )

            cluster_id = k8s.create_cluster(
                name=f'sawtooth{network_info["network_id"]}',
                cpu=network["node_infrastructure"]["node_plan"]["cpu"],
                ram=network["node_infrastructure"]["node_plan"]["ram"],
                number_nodes=network["node_infrastructure"]["number_vm_nodes"],
                digital_ocean_token=config["k8s"]["token"],
            )

            await self.__database.update_network(
                network_id=network_info["network_id"],
                modification={
                    "cluster_id": cluster_id,
                    "error": "",
                },
            )

            if "network_folder_id" not in network:
                token = get_token()["data"]["token"]
                user_folder = get_user_folder(token)
                network_folder_id = create_folder(
                    token,
                    {
                        "name": network_info["name"],
                        "parent_id": user_folder["folder_id"],
                        "shared": [user_info["user_id"]],
                    },
                )

                resources_folder_id = create_folder(
                    token,
                    {
                        "shared": [user_info["user_id"]],
                        "name": "resources",
                        "parent_id": network_folder_id,
                    },
                )

                await self.__database.update_network(
                    network_id=network_info["network_id"],
                    modification={
                        "network_folder_id": network_folder_id,
                        "resources_folder_id": resources_folder_id,
                    },
                )

            deploy_sawtooth.apply_async(
                args=[cluster_id, network, user_info, reply_to], queue="sawtooth.tasks"
            )

        except (ThirdPartyRequestError, NotSupported, ServiceError) as e:
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

    async def handle_network_error(self, body, reply_to, message_id):
        network_info = body["network_info"]
        user_info = body["user_info"]
        _LOGGER.debug(f"Receive message about network error")

        await self.__database.update_network(
            network_id=network_info["network_id"],
            modification={"error": network_info["error"]},
        )
