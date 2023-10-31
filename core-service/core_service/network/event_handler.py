from utils.logging import get_logger
from dapp.status import DappStatus
from network.status import NetworkStatus
from network.status import ResourceStatus
import json

_LOGGER = get_logger(__name__)


async def handle_create_network_event(body, reply_to, message_id, database):
    _LOGGER.debug("Receiving response about network creating process")
    
    if 'error' in body:
        user_id = body["error"]["user_id"]
        network_id = body["error"]["network_id"]
        await database.update_network(user_id=user_id,
                                      network_id=network_id,
                                      modification={"status": NetworkStatus.CREATE_FAIL.name,
                                                    "message": body["error"]["message"]})
    else:
        user_id = body["data"]["user_id"]
        network_id = body["data"]["network_id"]
        explorer_url = body["data"]["explorer_url"]
        modification = {
            "status": NetworkStatus.CREATED.name,
            "explorer_url": explorer_url
        }

        unset = {
            "message": ""
        }

        await database.update_network(user_id=user_id,
                                      network_id=network_id,
                                      modification=modification,
                                      unset=unset)


async def handle_delete_network_event(body, reply_to, message_id, database):
    _LOGGER.debug("Receiving response about network deleting process")
    
    if 'error' in body:
        user_id = body["error"]["user_id"]
        network_id = body["error"]["network_id"]
        # if "list_dapps" in body["error"]:
        #     for dapp in body["error"]["list_dapps"]:
        #         await database.update_dapp(dapp_id=dapp["dapp_id"],
        #                                     user_id=user_id,
        #                                     modification={"status": DappStatus.DELETE_FAIL.name,
        #                                                   "message": body["error"]["message"]})
        
        # if "deleted_dapps" in body["error"]:
        #     for dapp_id in body["error"]["deleted_dapps"]:
        #         await database.delete_dapp(dapp_id=dapp_id)
        # await database.update_network(user_id=user_id,
        #                               network_id=network_id,
        #                               modification={"status": NetworkStatus.DELETE_FAIL.name,
        #                                             "message": body["error"]["message"]})
        await database.delete_dapp(network_id=network_id)
        await database.delete_network(user_id=user_id, network_id=network_id)
        await database.delete_resource(network_id=network_id)
    else:
        user_id = body["data"]["user_id"]
        network_id = body["data"]["network_id"]
        await database.delete_dapp(network_id=network_id)
        await database.delete_network(user_id=user_id, network_id=network_id)
        await database.delete_resource(network_id=network_id)

async def handle_create_resource_event(body, reply_to, message_id, database):
    _LOGGER.debug("Receiving response about dapp creating process")
    
    if 'error' in body:
        user_id = body["error"]["user_id"]
        resource_id = body["error"]["resource_id"]
        await database.update_resource(user_id=user_id,
                                   resource_id=resource_id,
                                   modification={"status": ResourceStatus.CREATE_FAIL.name,
                                                 "message": body["error"]["message"]})
    else:
        user_id = body["data"]["user_id"]
        resource_id = body["data"]["resource_id"]
        modification = {
            "status": ResourceStatus.CREATED.name
        }
        if "resource_folder_id" in body["data"]:
            modification["resource_folder_id"] = body["data"]["resource_folder_id"]

        unset = {
            "message": ""
        }

        await database.update_resource(user_id=user_id,
                                   resource_id=resource_id,
                                   modification=modification,
                                   unset=unset)

async def handle_update_network_event(body, reply_to, message_id, database):
    _LOGGER.debug("Receiving response about network updating process")
    if 'error' in body:
        user_id = body["error"]["user_id"]
        network_id = body["error"]["network_id"]
        await database.update_network(user_id=user_id,
                                      network_id=network_id,
                                      modification={"status": NetworkStatus.UPDATE_FAIL.name,
                                                    "message": body["error"]["message"]})
    else:
        user_id = body["data"]["user_id"]
        network_id = body["data"]["network_id"]
        modification = body["data"]["new_network_config"]

        modification.pop("network_id", None)
        modification["status"] = NetworkStatus.CREATED.name

        unset = {
            "message": ""
        }
        await database.update_network(user_id=user_id,
                                      network_id=network_id,
                                      modification=modification,
                                      unset=unset)
