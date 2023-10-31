import os
import json
from pickle import TRUE
import shutil
import jwt

from includes import k8s
from settings import config
from includes.parser import gen_code
from worker.tasks import (
    git_push,
    git_push_without_create,
    task_upload_sdk,
    task_delete_folder,
    task_update_sdk,
)
from config.logging_config import get_logger
import constants
from exceptions import (
    SchemaError,
    StorageServiceRequestError,
    ServiceError,
    GitlabError,
    OperationError,
)
import includes.git_handler as git_handle
from includes.account_handler import *
from includes.storage_handler import create_folder, get_folder
from bson.objectid import ObjectId
import uuid
from operation import k8s_operation


_LOGGER = get_logger(__name__)


class DappHandler:
    def __init__(self, database, broker_client):
        self.__database = database
        self.__broker_client = broker_client

    async def handle_create_dapp(self, body, reply_to, message_id):
        try:
            dapp_info = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to create a dapp with dapp_id: {dapp_info['network_id']}"
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

            network = networks[0]
            network_folder_id = network["network_folder_id"]
            public_ip = k8s.get_public_ip(
                cluster_id=network["cluster_id"],
                digital_ocean_token=config["k8s"]["token"],
            )

            # Get token
            token = get_token()["data"]["token"]

            # Update dapp_name
            dapp_info["dapp_name"] = "{}-{}".format(
                dapp_info["dapp_name"], str(dapp_info["dapp_id"][-5:])
            )

            dapp_user_folder = f"application/{user_info['username']}"

            sdk_key = str(uuid.uuid4())

            await self.__database.create_dapp(
                {
                    "_id": ObjectId(dapp_info["dapp_id"]),
                    "dapp_name": dapp_info["dapp_name"],
                    "entities": dapp_info["entities"],
                    "encryption_type": dapp_info["encryption_type"],
                    "dapp_description": dapp_info["dapp_description"],
                    "user_id": user_info["user_id"],
                    "network_id": dapp_info["network_id"],
                    "sdk_key": sdk_key,
                    "dapp_version": 1,
                }
            )

            # Create dapp_folder_id
            dapp_folder_id = create_folder(
                token,
                {
                    "name": dapp_info["dapp_name"],
                    "parent_id": network_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            data_folder_id = create_folder(
                token,
                {
                    "name": "data",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            dapp_info["dapp_folder_id"] = dapp_folder_id
            dapp_info["data_folder_id"] = data_folder_id
            dapp_info["sdk_key"] = sdk_key
            dapp_info["dapp_version"] = 1
            dapp_info["old_protobufs"] = []

            # Create new record on mongo
            await self.__database.update_dapp(
                user_id=user_info["user_id"],
                dapp_id=dapp_info["dapp_id"],
                modification={
                    "dapp_folder_id": dapp_folder_id,
                    "data_folder_id": data_folder_id,
                },
            )

            user_groups = git_handle.get_groups(
                user_info["username"], config["gitlab"]["dapp_group_id"]
            )
            if len(user_groups) == 1:
                user_group_id = user_groups[0]["id"]
                user_info["user_group_id"] = user_group_id
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
                user_info["user_group_id"] = user_group_id
            else:
                _LOGGER.debug(
                    f"Have many groups on gitlab with name: {user_info['username']}"
                )
                raise ServiceError(
                    f"Have many groups on gitlab with name: {user_info['username']}"
                )

            parser_protobufs = await gen_code(
                dapp_info=dapp_info,
                user_info=user_info,
                number_peer=network["number_peer"],
                public_ip=public_ip,
                dst_folder=dapp_user_folder,
            )

            modification = {
                "protobufs": parser_protobufs
            }

            await self.__database.update_dapp(
                user_id=user_info["user_id"],
                dapp_id=dapp_info["dapp_id"],
                modification=modification,
            )

            # return success(swagger_data, app_name=nameModule)
            # is_update = False
            # push_to_git(dapp_info, user_info, dapp_user_folder, is_update, reply_to)

            # push sdk to storage
            sdk_folder_id = create_folder(
                token,
                {
                    "name": dapp_info["dapp_name"] + "sdk",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            # push proccess to storage
            proccessor_folder_id = create_folder(
                token,
                {
                    "name": dapp_info["dapp_name"] + "proccessor",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            sdk_path = os.path.join(
                constants.BASE_DIR,
                f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}sdk/',
            )
            processor_path = os.path.join(
                constants.BASE_DIR,
                f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}processor/',
            )
            task_upload_sdk.delay(
                token,
                user_info["user_id"],
                sdk_folder_id,
                sdk_path,
                data_folder_id,
                processor_path,
                user_info,
                dapp_info,
                dapp_folder_id,
                network["number_peer"],
                reply_to,
            )

            _LOGGER.info(f"Created dapp with dapp_id: {dapp_info['dapp_id']}")
        except (
            ServiceError,
            StorageServiceRequestError,
            GitlabError,
            SchemaError,
        ) as e:
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
            _LOGGER.debug(f"Fail to create dapp with dapp_id: {dapp_info['dapp_id']}")

    async def handle_update_dapp(self, body, reply_to, message_id):
        try:
            dapp_info = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to update a dapp with dapp_id: {dapp_info}"
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

            network = networks[0]
            network_folder_id = network["network_folder_id"]
            public_ip = k8s.get_public_ip(
                cluster_id=network["cluster_id"],
                digital_ocean_token=config["k8s"]["token"],
            )

            token = get_token()["data"]["token"]

            # dapp_code_folder = os.path.join(constants.BASE_DIR,
            #                                 'application/{0}/{1}'.format(user_info['username'],dapp_info['dapp_name']))

            # os.system("rm -rf " + dapp_code_folder)

            k8s_config_path = os.path.join(
                constants.BASE_DIR,
                "network/{}/{}/k8s_config.yaml".format(
                    user_info["username"], old_dapp["network_id"]
                ),
            )

            yaml_processor_path = os.path.join(
                constants.BASE_DIR,
                "application/{0}/{1}/{2}processor/processor.yaml".format(
                    user_info["username"], old_dapp["dapp_name"], old_dapp["dapp_name"]
                ),
            )
            deployment_name = old_dapp["dapp_name"] + "processorapp"
            check = k8s_operation.get_deployment(
                deployment_name=deployment_name, kube_config_path=k8s_config_path
            )
            
            if check != -1:

                # cmd = (
                #         "kubectl --kubeconfig " + k8s_config_path + " delete -f "
                #         + yaml_processor_path + " --namespace=default"
                # )
                # os.system(cmd)
                k8s_operation.delete_namespace(
                    file_path=yaml_processor_path, kube_config_path=k8s_config_path
                )

                # cmd2 = (
                #         "kubectl --kubeconfig " + k8s_config_path + " delete secret "
                #         + "deploy-" + dapp_info["dapp_name"] + "processor-secrets"
                # )
                secret_name = "deploy-" + old_dapp["dapp_name"] + "processor-secrets"
                k8s_operation.delete_secret(
                    secret_name=secret_name, kube_config_path=k8s_config_path
                )

                dapp_user_folder = f"application/{user_info['username']}"
                # Create dapp_folder_id
                dapp_folder_id = create_folder(
                    token,
                    {
                        "name": old_dapp["dapp_name"],
                        "parent_id": network_folder_id,
                        "shared": [user_info["user_id"]],
                    },
                )

                sdk_key = old_dapp["sdk_key"]

                data_folder_id = create_folder(
                    token,
                    {
                        "name": "data",
                        "parent_id": dapp_folder_id,
                        "shared": [user_info["user_id"]],
                    },
                )
                # Update record on mongo
                dapp_info["dapp_name"] = "{}-{}".format(
                    dapp_info["dapp_name"], str(dapp_info["dapp_id"][-5:])
                )
                dapp_info["data_folder_id"] = data_folder_id
                dapp_info["dapp_folder_id"] = dapp_folder_id
                dapp_info["sdk_key"] = sdk_key
                dapp_info["dapp_version"] = old_dapp["dapp_version"] + 1
                dapp_info["old_protobufs"] = old_dapp["protobufs"]

                modification = {
                    "dapp_description": dapp_info["dapp_description"],
                    "entities": dapp_info["entities"],
                    "encryption_type": dapp_info["encryption_type"],
                    "dapp_folder_id": dapp_folder_id,
                    "data_folder_id": data_folder_id,
                    "dapp_version": dapp_info["dapp_version"],
                    "old_dapp_description": old_dapp["dapp_description"],
                    "old_entities": old_dapp["entities"],
                    "old_encryption_type": old_dapp["encryption_type"],
                    "old_protobufs": old_dapp["protobufs"]
                }

                await self.__database.update_dapp(
                    user_id=user_info["user_id"],
                    dapp_id=dapp_info["dapp_id"],
                    modification=modification,
                )

                _LOGGER.debug(f"demoo-------------")

                parser_protobufs = await gen_code(
                    dapp_info=dapp_info,
                    user_info=user_info,
                    number_peer=network["number_peer"],
                    public_ip=public_ip,
                    dst_folder=dapp_user_folder,
                )

                modification = {
                    "protobufs": parser_protobufs
                }

                await self.__database.update_dapp(
                    user_id=user_info["user_id"],
                    dapp_id=dapp_info["dapp_id"],
                    modification=modification,
                )

                # push sdk to storage
                sdk_folder_id = create_folder(
                    token,
                    {
                        "name": dapp_info["dapp_name"] + "sdk",
                        "parent_id": dapp_folder_id,
                        "shared": [user_info["user_id"]],
                    },
                )

                # push proccess to storage
                proccessor_folder_id = create_folder(
                    token,
                    {
                        "name": dapp_info["dapp_name"] + "proccessor",
                        "parent_id": dapp_folder_id,
                        "shared": [user_info["user_id"]],
                    },
                )

                sdk_path = os.path.join(
                    constants.BASE_DIR,
                    f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}sdk/',
                )
                processor_path = os.path.join(
                    constants.BASE_DIR,
                    f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}processor/',
                )
                task_update_sdk.delay(
                    token,
                    user_info["user_id"],
                    old_dapp["dapp_folder_id"],
                    sdk_folder_id,
                    sdk_path,
                    data_folder_id,
                    processor_path,
                    user_info,
                    dapp_info,
                    dapp_folder_id,
                    network["number_peer"],
                    reply_to
                )
                _LOGGER.info(f"Created dapp with dapp_id: {dapp_info['dapp_id']}")
            else:
                failure_message = {
                    "error": {
                        "user_id": user_info["user_id"],
                        "dapp_id": dapp_info["dapp_id"],
                        "message": f"{deployment_name} is deploying",
                    }
                }
                await self.__broker_client.publish(
                    routing_key=reply_to, message=json.dumps(failure_message)
                )
                _LOGGER.debug(
                    f"Fail to update dapp with dapp_id: {dapp_info['dapp_id']}"
                )

        except (
            ServiceError,
            StorageServiceRequestError,
            GitlabError,
            OperationError,
            SchemaError,
        ) as e:
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

    async def handle_delete_dapp(self, body, reply_to, message_id):
        try:
            dapp_info = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to delete a dapp with dapp_id {dapp_info['dapp_id']}"
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

            dapp_info = dapps[0]

            k8s_config_path = os.path.join(
                constants.BASE_DIR,
                "network/{}/{}/k8s_config.yaml".format(
                    user_info["username"], dapp_info["network_id"]
                ),
            )

            yaml_processor_path = os.path.join(
                constants.BASE_DIR,
                "application/{0}/{1}/{2}processor/processor.yaml".format(
                    user_info["username"],
                    dapp_info["dapp_name"],
                    dapp_info["dapp_name"],
                ),
            )
            deployment_name = dapp_info["dapp_name"] + "processorapp"
            check = k8s_operation.get_deployment(
                deployment_name=deployment_name, kube_config_path=k8s_config_path
            )

            if check != -1:
                k8s_operation.delete_namespace(
                    file_path=yaml_processor_path, kube_config_path=k8s_config_path
                )

                secret_name = "deploy-" + dapp_info["dapp_name"] + "processor-secrets"
                k8s_operation.delete_secret(
                    secret_name=secret_name, kube_config_path=k8s_config_path
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

            token = get_token()["data"]["token"]
            if "dapp_folder_id" in dapp_info:
                dapp_folder_id = dapp_info["dapp_folder_id"]
            else:
                dapp_folder_id = -1

            task_delete_folder.delay(
                token, dapp_folder_id, user_info, dapp_info, reply_to
            )

            await self.__database.delete_dapp(
                dapp_id=dapp_info["dapp_id"], user_id=user_info["user_id"]
            )

            dapp_code_folder = os.path.join(
                constants.BASE_DIR,
                "application/{0}/{1}".format(
                    user_info["username"], dapp_info["dapp_name"]
                ),
            )

            # os.system("rm -rf " + dapp_code_folder)
            if os.path.exists(dapp_code_folder):
                shutil.rmtree(dapp_code_folder)

            _LOGGER.debug(f"Deleted dapp with dapp_id: {dapp_info['dapp_id']}")

        except (
            ServiceError,
            StorageServiceRequestError,
            GitlabError,
            OperationError,
        ) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "dapp_id": dapp_info["dapp_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(f"Fail to delete dapp with dapp_id: {dapp_info['dapp_id']}")

    async def handle_retry_create_dapp(self, body, reply_to, message_id):
        try:
            dapp_info = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to retry a dapp with dapp_id: {dapp_info}"
            )

            dapps = await self.__database.get_dapps(dapp_id=dapp_info["dapp_id"])
            if len(dapps) > 1:
                raise ServiceError(
                    f"Have more than one dapp with dapp_id: {dapp_info['dapp_id']}"
                )
            elif len(dapps) == 0:
                raise ServiceError(
                    f"Don't have network with network_id: {dapp_info['dapp_id']}"
                )

            dapp = dapps[0]
            dapp["dapp_id"] = dapp_info["dapp_id"]

            networks = await self.__database.get_networks(network_id=dapp["network_id"])
            if len(networks) > 1:
                raise ServiceError(
                    f"Have more than one network with network_id: {dapp['network_id']}"
                )
            elif len(networks) == 0:
                raise ServiceError(
                    f"Don't have network with network_id: {dapp['network_id']}"
                )

            network = networks[0]
            network_folder_id = network["network_folder_id"]
            public_ip = k8s.get_public_ip(
                cluster_id=network["cluster_id"],
                digital_ocean_token=config["k8s"]["token"],
            )

            token = get_token()["data"]["token"]

            k8s_config_path = os.path.join(
                constants.BASE_DIR,
                "network/{}/{}/k8s_config.yaml".format(
                    user_info["username"], dapp["network_id"]
                ),
            )

            yaml_processor_path = os.path.join(
                constants.BASE_DIR,
                "application/{0}/{1}/{2}processor/processor.yaml".format(
                    user_info["username"], dapp["dapp_name"], dapp["dapp_name"]
                ),
            )
            deployment_name = dapp["dapp_name"] + "processorapp"

            check = k8s_operation.get_deployment(
                deployment_name=deployment_name, kube_config_path=k8s_config_path
            )

            if check != -1:
                k8s_operation.delete_namespace(
                    file_path=yaml_processor_path, kube_config_path=k8s_config_path
                )
                secret_name = "deploy-" + dapp["dapp_name"] + "processor-secrets"
                k8s_operation.delete_secret(
                    secret_name=secret_name, kube_config_path=k8s_config_path
                )

            old_dapp_folder = os.path.join(
                constants.BASE_DIR,
                "application/{0}/{1}".format(user_info["username"], dapp["dapp_name"]),
            )

            if os.path.exists(old_dapp_folder):
                shutil.rmtree(old_dapp_folder)

            user_groups = git_handle.get_groups(
                user_info["username"], config["gitlab"]["dapp_group_id"]
            )
            if len(user_groups) == 1:
                user_group_id = user_groups[0]["id"]
                user_info["user_group_id"] = user_group_id
                dapp_groups = git_handle.get_groups(dapp["dapp_name"], user_group_id)
                if len(dapp_groups) == 1:
                    git_handle.delete_group(dapp_groups[0]["id"])
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
                user_info["user_group_id"] = user_group_id
            else:
                _LOGGER.debug(
                    f"Have many groups on gitlab with name: {user_info['username']}"
                )
                raise ServiceError(
                    f"Have many groups on gitlab with name: {user_info['username']}"
                )

            dapp_user_folder = f"application/{user_info['username']}"

            dapp["retry"] = "yes"
            dapp["old_protobufs"] = []
            
            # Create dapp_folder_id

            if "dapp_folder_id" not in dapp:
                old_folder_id = -1
            else:
                old_folder_id = dapp["dapp_folder_id"]

            dapp_folder_id = create_folder(
                token,
                {
                    "name": dapp["dapp_name"],
                    "parent_id": network_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            data_folder_id = create_folder(
                token,
                {
                    "name": "data",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            modification = {
                "dapp_folder_id": dapp_folder_id,
                "data_folder_id": data_folder_id,
            }

            # Update record on mongo
            await self.__database.update_dapp(
                user_id=user_info["user_id"],
                dapp_id=dapp_info["dapp_id"],
                modification=modification,
            )

            # Gen code
            parser_protobufs = await gen_code(
                dapp_info=dapp,
                user_info=user_info,
                number_peer=network["number_peer"],
                public_ip=public_ip,
                dst_folder=dapp_user_folder,
            )

            modification = {
                "protobufs": parser_protobufs
            }

            # Update record on mongo
            await self.__database.update_dapp(
                user_id=user_info["user_id"],
                dapp_id=dapp_info["dapp_id"],
                modification=modification,
            )


            # push to storage
            sdk_folder_id = create_folder(
                token,
                {
                    "name": dapp["dapp_name"] + "sdk",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            proccessor_folder_id = create_folder(
                token,
                {
                    "name": dapp["dapp_name"] + "proccessor",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            sdk_path = os.path.join(
                constants.BASE_DIR,
                f'{dapp_user_folder}/{dapp["dapp_name"]}/{dapp["dapp_name"]}sdk/',
            )
            processor_path = os.path.join(
                constants.BASE_DIR,
                f'{dapp_user_folder}/{dapp["dapp_name"]}/{dapp["dapp_name"]}processor/',
            )

            task_update_sdk.delay(
                token,
                user_info["user_id"],
                old_folder_id,
                sdk_folder_id,
                sdk_path,
                data_folder_id,
                processor_path,
                user_info,
                dapp,
                dapp_folder_id,
                network["number_peer"],
                reply_to,
            )
            _LOGGER.info(f"Created dapp with dapp_id: {dapp_info['dapp_id']}")

        except (
            ServiceError,
            StorageServiceRequestError,
            GitlabError,
            OperationError,
            SchemaError,
        ) as e:
            failure_message = {
                "error": {
                    "user_id": user_info["user_id"],
                    "dapp_id": dapp_info["dapp_id"],
                    "message": e.message,
                }
            }
            await self.__broker_client.publish(
                routing_key=reply_to, message=json.dumps(failure_message)
            )
            _LOGGER.debug(
                f"Fail to retry create dapp with dapp_id: {dapp_info['dapp_id']}"
            )

    async def handle_retry_update_dapp(self, body, reply_to, message_id):
        try:
            dapp_info = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to update a dapp with dapp_id: {dapp_info}"
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

            network = networks[0]
            network_folder_id = network["network_folder_id"]
            public_ip = k8s.get_public_ip(
                cluster_id=network["cluster_id"],
                digital_ocean_token=config["k8s"]["token"],
            )

            token = get_token()["data"]["token"]

            k8s_config_path = os.path.join(
                constants.BASE_DIR,
                "network/{}/{}/k8s_config.yaml".format(
                    user_info["username"], old_dapp["network_id"]
                ),
            )

            yaml_processor_path = os.path.join(
                constants.BASE_DIR,
                "application/{0}/{1}/{2}processor/processor.yaml".format(
                    user_info["username"], old_dapp["dapp_name"], old_dapp["dapp_name"]
                ),
            )

            # Delete deployment in k8s
            deployment_name = old_dapp["dapp_name"] + "processorapp"
            check = k8s_operation.get_deployment(
                deployment_name=deployment_name, kube_config_path=k8s_config_path
            )

            if check != -1:
                k8s_operation.delete_namespace(
                    file_path=yaml_processor_path, kube_config_path=k8s_config_path
                )
            # Delete secret in k8s
            secret_name = "deploy-" + old_dapp["dapp_name"] + "processor-secrets"
            check = k8s_operation.get_secret(
                secret_name=secret_name, kube_config_path=k8s_config_path
            )
            if check != -1:
                k8s_operation.delete_secret(
                    secret_name=secret_name, kube_config_path=k8s_config_path
                )

            dapp_user_folder = f"application/{user_info['username']}"

            # Create dapp_folder_id
            if "dapp_folder_id" not in old_dapp:
                old_folder_id = -1
            else:
                old_folder_id = old_dapp["dapp_folder_id"]

            dapp_folder_id = create_folder(
                token,
                {
                    "name": old_dapp["dapp_name"],
                    "parent_id": network_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            data_folder_id = create_folder(
                token,
                {
                    "name": "data",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )
            # Update record on mongo
            dapp_info = old_dapp
            dapp_info["data_folder_id"] = data_folder_id
            dapp_info["dapp_folder_id"] = dapp_folder_id
            dapp_info["old_protobufs"] = old_dapp["old_protobufs"]

            modification = {
                "dapp_folder_id": dapp_folder_id,
                "data_folder_id": data_folder_id,
            }

            await self.__database.update_dapp(
                user_id=user_info["user_id"],
                dapp_id=dapp_info["dapp_id"],
                modification=modification,
            )


            parser_protobufs =  await gen_code(
                dapp_info=dapp_info,
                user_info=user_info,
                number_peer=network["number_peer"],
                public_ip=public_ip,
                dst_folder=dapp_user_folder,
            )

            modification = {
                "old_protobufs": parser_protobufs
            }

            await self.__database.update_dapp(
                user_id=user_info["user_id"],
                dapp_id=dapp_info["dapp_id"],
                modification=modification,
            )

            # push sdk to storage
            sdk_folder_id = create_folder(
                token,
                {
                    "name": dapp_info["dapp_name"] + "sdk",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            # push proccess to storage
            proccessor_folder_id = create_folder(
                token,
                {
                    "name": dapp_info["dapp_name"] + "proccessor",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            sdk_path = os.path.join(
                constants.BASE_DIR,
                f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}sdk/',
            )
            processor_path = os.path.join(
                constants.BASE_DIR,
                f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}processor/',
            )
            task_update_sdk.delay(
                token,
                user_info["user_id"],
                old_folder_id,
                sdk_folder_id,
                sdk_path,
                data_folder_id,
                processor_path,
                user_info,
                dapp_info,
                dapp_folder_id,
                network["number_peer"],
                reply_to,
            )
            _LOGGER.info(f"Updated dapp with dapp_id: {dapp_info['dapp_id']}")

        except (
            ServiceError,
            StorageServiceRequestError,
            GitlabError,
            OperationError,
            SchemaError,
        ) as e:
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
            _LOGGER.debug(
                f"Fail to retry update dapp with dapp_id: {dapp_info['dapp_id']}"
            )

    async def handle_rollback_dapp(self, body, reply_to, message_id):
        try:
            dapp_info = body["dapp_info"]
            user_info = body["user_info"]
            _LOGGER.debug(
                f"Receive a request to update a dapp with dapp_id: {dapp_info}"
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
            # Update dapp_name
            dapp_info["dapp_name"] = "{}-{}".format(
                dapp_info["dapp_name"], str(dapp_info["dapp_id"][-5:])
            )

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

            network = networks[0]
            network_folder_id = network["network_folder_id"]
            public_ip = k8s.get_public_ip(
                cluster_id=network["cluster_id"],
                digital_ocean_token=config["k8s"]["token"],
            )

            token = get_token()["data"]["token"]

            k8s_config_path = os.path.join(
                constants.BASE_DIR,
                "network/{}/{}/k8s_config.yaml".format(
                    user_info["username"], old_dapp["network_id"]
                ),
            )

            yaml_processor_path = os.path.join(
                constants.BASE_DIR,
                "application/{0}/{1}/{2}processor/processor.yaml".format(
                    user_info["username"], old_dapp["dapp_name"], old_dapp["dapp_name"]
                ),
            )

            # Delete deployment in k8s
            deployment_name = old_dapp["dapp_name"] + "processorapp"
            check = k8s_operation.get_deployment(
                deployment_name=deployment_name, kube_config_path=k8s_config_path
            )
            _LOGGER.debug("check:" + str(check))

            if check != -1:
                k8s_operation.delete_namespace(
                    file_path=yaml_processor_path, kube_config_path=k8s_config_path
                )
            # Delete secret in k8s
            secret_name = "deploy-" + old_dapp["dapp_name"] + "processor-secrets"
            check = k8s_operation.get_secret(
                secret_name=secret_name, kube_config_path=k8s_config_path
            )
            if check != -1:
                k8s_operation.delete_secret(
                    secret_name=secret_name, kube_config_path=k8s_config_path
                )

            dapp_user_folder = f"application/{user_info['username']}"

            # Create dapp_folder_id
            if "dapp_folder_id" not in old_dapp:
                old_folder_id = -1
            else:
                old_folder_id = old_dapp["dapp_folder_id"]

            dapp_folder_id = create_folder(
                token,
                {
                    "name": old_dapp["dapp_name"],
                    "parent_id": network_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            data_folder_id = create_folder(
                token,
                {
                    "name": "data",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            # Update record on mongo
            dapp_info["data_folder_id"] = data_folder_id
            dapp_info["dapp_folder_id"] = dapp_folder_id
            dapp_info["rollback"] = True
            dapp_info["sdk_key"] = old_dapp["sdk_key"]
            if "old_protobufs" in old_dapp:
                dapp_info["old_protobufs"] = old_dapp["old_protobufs"]
            else:
                dapp_info["old_protobufs"] = []

            _LOGGER.debug(f"dapp info roll back: {dapp_info}")

            modification = {
                "dapp_folder_id": dapp_folder_id,
                "data_folder_id": data_folder_id,
                "dapp_version": dapp_info["dapp_version"],
                
                "old_dapp_description": "",
                "old_entities": "",
                "old_encryption_type": ""
            }

            await self.__database.update_dapp(
                user_id=user_info["user_id"],
                dapp_id=dapp_info["dapp_id"],
                modification=modification,
            )

            parser_protobufs = await gen_code(
                dapp_info=dapp_info,
                user_info=user_info,
                number_peer=network["number_peer"],
                public_ip=public_ip,
                dst_folder=dapp_user_folder,
            )

            modification = {
                "protobufs": parser_protobufs
            }

            await self.__database.update_dapp(
                user_id=user_info["user_id"],
                dapp_id=dapp_info["dapp_id"],
                modification=modification,
            )


            # push sdk to storage
            sdk_folder_id = create_folder(
                token,
                {
                    "name": dapp_info["dapp_name"] + "sdk",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            # push proccess to storage
            proccessor_folder_id = create_folder(
                token,
                {
                    "name": dapp_info["dapp_name"] + "proccessor",
                    "parent_id": dapp_folder_id,
                    "shared": [user_info["user_id"]],
                },
            )

            sdk_path = os.path.join(
                constants.BASE_DIR,
                f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}sdk/',
            )
            processor_path = os.path.join(
                constants.BASE_DIR,
                f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}processor/',
            )
            task_update_sdk.delay(
                token,
                user_info["user_id"],
                old_folder_id,
                sdk_folder_id,
                sdk_path,
                data_folder_id,
                processor_path,
                user_info,
                dapp_info,
                dapp_folder_id,
                network["number_peer"],
                reply_to,
            )
            _LOGGER.info(f"Updated dapp with dapp_id: {dapp_info['dapp_id']}")

        except (
            ServiceError,
            StorageServiceRequestError,
            GitlabError,
            OperationError,
            SchemaError,
        ) as e:
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
            _LOGGER.debug(
                f"Fail to rollback dapp with dapp_id: {dapp_info['dapp_id']}"
            )


def push_to_git(dapp_info, user_info, dapp_user_folder, is_update, reply_to):
    sdk_path = os.path.join(
        constants.BASE_DIR,
        f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}sdk/',
    )
    sdk_project_name = dapp_info["dapp_name"] + "sdk"

    processor_path = os.path.join(
        constants.BASE_DIR,
        f'{dapp_user_folder}/{dapp_info["dapp_name"]}/{dapp_info["dapp_name"]}processor/',
    )
    processor_project_name = dapp_info["dapp_name"] + "processor"

    if is_update:
        git_push_without_create.delay(
            user_info["username"], sdk_path, processor_path, "update dapp"
        )
    else:
        git_push.delay(
            user_id=user_info["user_id"],
            dapp_id=dapp_info["dapp_id"],
            username=user_info["username"],
            dapp_name=dapp_info["dapp_name"],
            network_id=dapp_info["network_id"],
            sdk_path=sdk_path,
            processor_path=processor_path,
            sdk_project_name=sdk_project_name,
            processor_project_name=processor_project_name,
            commit_message="create dapp",
            reply_to=reply_to,
        )
