import os
import uuid
import copy
import json
from bson.objectid import ObjectId
from utils.logging import get_logger
import const
from settings import config
from exceptions import ThirdPartyRequestError, ServiceError, NotSupported
from aiohttp.web import json_response
from celery_worker.tasks import (
    generate_chaincode_file,
    update_chaincode,
    rollback_chaincode,
    delete_dapp_folder,
    delete_dapp_gitlab,
)
from account import account_handler
from storage import storage_handler
from utils import get_folder_path
from dapp.error import ChaincodeOpErrorStatus

_LOGGER = get_logger(__name__)


class DappHandler:
    def __init__(self, database, broker_client):
        self.__database = database
        self.__broker_client = broker_client

    async def handle_create_dapp(self, body, reply_to, message_id):
        try:
            new_dapp = body["dapp_info"]
            new_dapp["dapp_name"] = "{}-{}".format(
                new_dapp["dapp_name"], str(new_dapp["dapp_id"])[-5:]
            )
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to create a dapp with dapp_id: {new_dapp['dapp_id']}"
            )

            networks = await self.__database.get_networks(
                network_id=new_dapp["network_id"]
            )
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {new_dapp['network_id']}"
                )
            elif len(networks) == 0:
                raise ServiceError(
                    f"Don't have network with network_id: {new_dapp['network_id']}"
                )

            network_config = networks[0]
            network_config["network_id"] = new_dapp["network_id"]

            new_dapp["dapp_version"] = 1

            sdk_key = str(uuid.uuid4())

            new_dapp["sdk_key"] = sdk_key

            await self.__database.create_dapp(
                {
                    "_id": ObjectId(new_dapp["dapp_id"]),
                    "dapp_name": new_dapp["dapp_name"],
                    "dapp_description": new_dapp["dapp_description"],
                    "dapp_version": new_dapp["dapp_version"],
                    "entities": new_dapp["entities"],
                    "network_id": new_dapp["network_id"],
                    # "dapp_folder_id": new_dapp["dapp_folder_id"],
                    "user_id": user_info["user_id"],
                    "sdk_key": new_dapp["sdk_key"],
                    "encryption_type": new_dapp["encryption_type"]
                    if "encryption_type" in new_dapp
                    else "",
                }
            )

            token = account_handler.get_token()

            dapp_folder_id = storage_handler.create_folder(
                token,
                {
                    "name": new_dapp["dapp_name"],
                    "parent_id": network_config["network_folder_id"],
                    "shared": [user_info["user_id"]],
                },
            )

            modification = {
                "dapp_folder_id": dapp_folder_id,
            }

            await self.__database.update_dapp(
                dapp_id=new_dapp["dapp_id"], modification=modification
            )

            new_dapp["dapp_folder_id"] = dapp_folder_id

            dapp_folder = get_folder_path.get_dapp_folder_path(
                username=user_info["username"],
                network_id=network_config["network_id"],
                dapp_name=new_dapp["dapp_name"],
            )

            if not os.path.exists(dapp_folder):
                _LOGGER.debug(f"Create folder: {dapp_folder}")
                os.makedirs(dapp_folder)

            kube_config_path = os.path.join(
                get_folder_path.get_kube_config_folder_path(
                    username=user_info["username"],
                    network_id=network_config["network_id"],
                ),
                "k8s_config.yaml",
            )

            generate_chaincode_file.delay(
                network_config=network_config,
                dapp_config=new_dapp,
                dapp_folder=dapp_folder,
                user_info=user_info,
                kube_config_path=kube_config_path,
                token=token,
                dapp_folder_id=new_dapp["dapp_folder_id"],
                sdk_key=new_dapp["sdk_key"],
                dapp_version=new_dapp["dapp_version"],
                reply_to=reply_to,
            )

        except ThirdPartyRequestError as e:

            modification = {
                "error": {"code": ChaincodeOpErrorStatus.PRE_ERROR.name, "info": None}
            }

            await self.__database.update_dapp(
                dapp_id=new_dapp["dapp_id"], modification=modification
            )

            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": new_dapp["network_id"],
                    "dapp_id": new_dapp["dapp_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to create dapp with dapp_id: {new_dapp['dapp_id']}")

    async def handle_update_dapp(self, body, reply_to, message_id):
        try:
            new_dapp = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to update a dapp with dapp_id: {new_dapp['dapp_id']}"
            )

            dapps = await self.__database.get_dapps(dapp_id=new_dapp["dapp_id"])

            if len(dapps) > 1:
                raise ServiceError(
                    f"Have more than one dapp with dapp_id: {new_dapp['dapp_id']}"
                )
            elif len(dapps) == 0:
                raise ServiceError(
                    f"Don't have dapp with dapp_id: {new_dapp['dapp_id']}"
                )

            old_dapp = dapps[0]

            networks = await self.__database.get_networks(
                network_id=new_dapp["network_id"]
            )
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {new_dapp['network_id']}"
                )
            elif len(networks) == 0:
                raise ServiceError(
                    f"Don't have network with network_id: {new_dapp['network_id']}"
                )

            network_config = networks[0]
            network_config["network_id"] = new_dapp["network_id"]

            token = account_handler.get_token()

            new_dapp["dapp_name"] = old_dapp["dapp_name"]

            if "encryption_type" not in new_dapp:
                new_dapp["encryption_type"] = old_dapp["encryption_type"]

            dapp_folder_id = old_dapp["dapp_folder_id"]
            sdk_key = old_dapp["sdk_key"]

            kube_config_path = os.path.join(
                get_folder_path.get_kube_config_folder_path(
                    username=user_info["username"],
                    network_id=network_config["network_id"],
                ),
                "k8s_config.yaml",
            )

            dapp_folder = get_folder_path.get_dapp_folder_path(
                username=user_info["username"],
                network_id=network_config["network_id"],
                dapp_name=new_dapp["dapp_name"],
            )

            modification = {
                "dapp_description": new_dapp["dapp_description"],
                "entities": new_dapp["entities"],
                "dapp_version": new_dapp["dapp_version"],
                "encryption_type": new_dapp["encryption_type"],
            }

            await self.__database.update_dapp(
                dapp_id=new_dapp["dapp_id"], modification=modification
            )

            update_chaincode.delay(
                network_config=network_config,
                dapp_config=new_dapp,
                dapp_folder=dapp_folder,
                user_info=user_info,
                kube_config_path=kube_config_path,
                token=token,
                dapp_folder_id=dapp_folder_id,
                sdk_key=sdk_key,
                dapp_version=new_dapp["dapp_version"],
                reply_to=reply_to,
            )

        except ThirdPartyRequestError as e:
            modification = {
                "error": {"code": ChaincodeOpErrorStatus.PRE_ERROR.name, "info": None}
            }

            await self.__database.update_dapp(
                dapp_id=new_dapp["dapp_id"], modification=modification
            )

            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": new_dapp["network_id"],
                    "dapp_id": new_dapp["dapp_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to update dapp with dapp_id: {new_dapp['dapp_id']}")

    async def handle_retry_dapp(self, body, reply_to, message_id):
        try:
            dapp_info = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to retry create a dapp with dapp_id: {dapp_info['dapp_id']}"
            )

            dapps = await self.__database.get_dapps(dapp_id=dapp_info["dapp_id"])

            if len(dapps) > 1:
                raise ServiceError(
                    f"Have more than one dapp with dapp_id: {dapp_info['dapp_id']}"
                )
            elif len(dapps) == 0:
                raise ServiceError(
                    f"Don't have dapp with dapp_id: {dapp_info['dapp_id']}"
                )

            old_dapp = dapps[0]

            networks = await self.__database.get_networks(
                network_id=old_dapp["network_id"]
            )
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {old_dapp['network_id']}"
                )
            elif len(networks) == 0:
                raise ServiceError(
                    f"Don't have network with network_id: {old_dapp['network_id']}"
                )

            network_config = networks[0]
            network_config["network_id"] = old_dapp["network_id"]

            if "error" not in old_dapp:
                raise NotSupported(f"No Error found yet")

            if not old_dapp["error"]:
                raise NotSupported(f"No Error found yet")

            token = account_handler.get_token()

            if "dapp_folder_id" not in old_dapp:
                dapp_folder_id = storage_handler.create_folder(
                    token,
                    {
                        "name": old_dapp["dapp_name"],
                        "parent_id": network_config["network_folder_id"],
                        "shared": [user_info["user_id"]],
                    },
                )

                modification = {
                    "dapp_folder_id": dapp_folder_id,
                }

                await self.__database.update_dapp(
                    dapp_id=old_dapp["dapp_id"], modification=modification
                )

            else:
                dapp_folder_id = old_dapp["dapp_folder_id"]

            sdk_key = old_dapp["sdk_key"]

            kube_config_path = os.path.join(
                get_folder_path.get_kube_config_folder_path(
                    username=user_info["username"],
                    network_id=network_config["network_id"],
                ),
                "k8s_config.yaml",
            )

            dapp_folder = get_folder_path.get_dapp_folder_path(
                username=user_info["username"],
                network_id=network_config["network_id"],
                dapp_name=old_dapp["dapp_name"],
            )

            modification = {"error": None}

            await self.__database.update_dapp(
                dapp_id=old_dapp["dapp_id"], modification=modification
            )

            if old_dapp["dapp_version"] == 1:
                generate_chaincode_file.delay(
                    network_config=network_config,
                    dapp_config=old_dapp,
                    dapp_folder=dapp_folder,
                    user_info=user_info,
                    kube_config_path=kube_config_path,
                    token=token,
                    dapp_folder_id=dapp_folder_id,
                    sdk_key=sdk_key,
                    dapp_version=old_dapp["dapp_version"],
                    reply_to=reply_to,
                    error=old_dapp["error"],
                )
            else:
                update_chaincode.delay(
                    network_config=network_config,
                    dapp_config=old_dapp,
                    dapp_folder=dapp_folder,
                    user_info=user_info,
                    kube_config_path=kube_config_path,
                    token=token,
                    dapp_folder_id=dapp_folder_id,
                    sdk_key=sdk_key,
                    dapp_version=old_dapp["dapp_version"],
                    reply_to=reply_to,
                    error=old_dapp["error"],
                )

        except ThirdPartyRequestError as e:

            modification = {
                "error": {"code": ChaincodeOpErrorStatus.PRE_ERROR.name, "info": None}
            }

            await self.__database.update_dapp(
                dapp_id=old_dapp["dapp_id"], modification=modification
            )

            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": dapp_info["network_id"],
                    "dapp_id": dapp_info["dapp_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to update dapp with dapp_id: {dapp_info['dapp_id']}")

        except Exception as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": dapp_info["network_id"],
                    "dapp_id": dapp_info["dapp_id"],
                    "message": "Fail to update dapp",
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to update dapp with dapp_id: {dapp_info['dapp_id']}")

    async def handle_rollback_dapp(self, body, reply_to, message_id):
        try:
            new_dapp = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to update a dapp with dapp_id: {new_dapp['dapp_id']}"
            )

            dapps = await self.__database.get_dapps(dapp_id=new_dapp["dapp_id"])

            if len(dapps) > 1:
                raise ServiceError(
                    f"Have more than one dapp with dapp_id: {new_dapp['dapp_id']}"
                )
            elif len(dapps) == 0:
                raise ServiceError(
                    f"Don't have dapp with dapp_id: {new_dapp['dapp_id']}"
                )

            old_dapp = dapps[0]

            networks = await self.__database.get_networks(
                network_id=new_dapp["network_id"]
            )
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {new_dapp['network_id']}"
                )
            elif len(networks) == 0:
                raise ServiceError(
                    f"Don't have network with network_id: {new_dapp['network_id']}"
                )

            network_config = networks[0]
            network_config["network_id"] = new_dapp["network_id"]

            token = account_handler.get_token()

            new_dapp["dapp_name"] = old_dapp["dapp_name"]

            if "encryption_type" not in new_dapp:
                new_dapp["encryption_type"] = old_dapp["encryption_type"]

            dapp_folder_id = old_dapp["dapp_folder_id"]
            sdk_key = old_dapp["sdk_key"]

            kube_config_path = os.path.join(
                get_folder_path.get_kube_config_folder_path(
                    username=user_info["username"],
                    network_id=network_config["network_id"],
                ),
                "k8s_config.yaml",
            )

            dapp_folder = get_folder_path.get_dapp_folder_path(
                username=user_info["username"],
                network_id=network_config["network_id"],
                dapp_name=new_dapp["dapp_name"],
            )

            modification = {
                "dapp_description": new_dapp["dapp_description"],
                "entities": new_dapp["entities"],
                "dapp_version": new_dapp["dapp_version"],
                "encryption_type": new_dapp["encryption_type"],
            }

            await self.__database.update_dapp(
                dapp_id=new_dapp["dapp_id"], modification=modification
            )

            rollback_chaincode.delay(
                network_config=network_config,
                dapp_config=new_dapp,
                dapp_folder=dapp_folder,
                user_info=user_info,
                kube_config_path=kube_config_path,
                token=token,
                dapp_folder_id=dapp_folder_id,
                sdk_key=sdk_key,
                dapp_version=new_dapp["dapp_version"],
                reply_to=reply_to,
            )

        except ThirdPartyRequestError as e:
            modification = {
                "error": {"code": ChaincodeOpErrorStatus.PRE_ERROR.name, "info": None}
            }

            await self.__database.update_dapp(
                dapp_id=new_dapp["dapp_id"], modification=modification
            )

            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": new_dapp["network_id"],
                    "dapp_id": new_dapp["dapp_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to update dapp with dapp_id: {new_dapp['dapp_id']}")

    async def handle_delete_dapp(self, body, reply_to, message_id):
        try:
            dapp_info = body["dapp_info"]
            dapp_info["dapp_name"] = "{}-{}".format(
                dapp_info["dapp_name"], str(dapp_info["dapp_id"])[-5:]
            )
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to delete a dapp with dapp_id: {dapp_info['dapp_id']}"
            )

            success_message = {
                "data": {
                    "user_id": user_info["user_id"],
                    "network_id": dapp_info["network_id"],
                    "dapp_id": dapp_info["dapp_id"],
                }
            }

            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(success_message)
            )

            networks = await self.__database.get_networks(
                network_id=dapp_info["network_id"]
            )
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {dapp_info['network_id']}"
                )
            elif len(networks) == 0:
                raise ServiceError(
                    f"Don't have network with network_id: {dapp_info['network_id']}"
                )
            network_config = networks[0]
            network_config["network_id"] = dapp_info["network_id"]

            dapps = await self.__database.get_dapps(
                network_id=dapp_info["network_id"], dapp_id=dapp_info["dapp_id"]
            )

            if len(dapps) > 1:
                raise ServiceError(
                    f"Have more than one dapp with dapp_id: {dapp_info['dapp_id']}"
                )
            elif len(dapps) == 0:
                raise ServiceError(
                    f"Don't have dapp with dapp_id: {dapp_info['dapp_id']}"
                )
            dapp = dapps[0]
            dapp["dapp_id"] = dapp_info["dapp_id"]

            storage_handler.delete_folder(
                account_handler.get_token(),
                dapp["dapp_folder_id"],
            )

            await self.__database.delete_dapp(dapp_id=dapp_info["dapp_id"])

            delete_dapp_gitlab.delay(dapp_id=dapp_info["dapp_id"])

            delete_dapp_folder.delay(
                network_info=network_config,
                user_info=user_info,
                dapp_info=dapp_info,
            )

        except ThirdPartyRequestError as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "network_id": dapp_info["network_id"],
                    "dapp_id": dapp_info["dapp_id"],
                    "message": e.message,
                }
            }
            # await self.__broker_client.publish(
            #     routing_key=reply_to, message=json.dumps(failure_message)
            # )
            _LOGGER.debug(f"Fail to delete dapp with dapp_id: {dapp_info['dapp_id']}")

    async def handle_dapp_error(self, body, reply_to, message_id):
        dapp_info = body["dapp_info"]
        user_info = body["user_info"]
        _LOGGER.debug(f"Receive message about dapp error")

        modification = copy.deepcopy(dapp_info)

        modification.pop("dapp_id", None)

        await self.__database.update_dapp(
            user_id=user_info["user_id"],
            dapp_id=dapp_info["dapp_id"],
            modification=modification,
        )
