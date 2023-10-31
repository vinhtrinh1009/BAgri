import json

from utils.logging import get_logger
from dapp.status import DappStatus

_LOGGER = get_logger(__name__)


async def handle_create_dapp_event(body, reply_to, message_id, database):
    _LOGGER.debug("Receiving response about dapp creating process")
    
    if 'error' in body:
        user_id = body["error"]["user_id"]
        dapp_id = body["error"]["dapp_id"]
        await database.update_dapp(user_id=user_id,
                                   dapp_id=dapp_id,
                                   modification={"status": DappStatus.CREATE_FAIL.name,
                                                 "message": body["error"]["message"]})
    else:
        user_id = body["data"]["user_id"]
        dapp_id = body["data"]["dapp_id"]
        modification = {
            "status": DappStatus.CREATED.name
        }
        if "sdk_folder_id" in body["data"]:
            modification["sdk_folder_id"] = body["data"]["sdk_folder_id"]
        if "data_folder_id" in body["data"]:
            modification["data_folder_id"] = body["data"]["data_folder_id"]
        if "sdk_key" in body["data"]:
            modification["sdk_key"] = body["data"]["sdk_key"]
        if "smart_contract_address" in body["data"]:
            modification["smart_contract_address"] = body["data"]["smart_contract_address"]

        unset = {
            "message": ""
        }

        await database.update_dapp(user_id=user_id,
                                   dapp_id=dapp_id,
                                   modification=modification,
                                   unset=unset)

async def handle_update_dapp_event(body, reply_to, message_id, database):
    _LOGGER.debug("Receiving response about dapp updating process")
    
    if 'error' in body:
        user_id = body["error"]["user_id"]
        dapp_id = body["error"]["dapp_id"]
        await database.update_dapp(user_id=user_id,
                                   dapp_id=dapp_id,
                                   modification={"status": DappStatus.UPDATE_FAIL.name,
                                                 "message": body["error"]["message"]})
    else:
        user_id = body["data"]["user_id"]
        dapp_id = body["data"]["dapp_id"]
        modification = {
            "status": DappStatus.CREATED.name,
            "dapp_version": body["data"]["dapp_version"],
            
        }
        unset = {
            "temp_dapp_logo": "",
            "temp_entities": "",
            "temp_diagrams": "",
            "temp_dapp_description": "",
            "message": ""
        }
        if "sdk_folder_id" in body["data"]:
            modification["sdk_folder_id"] = body["data"]["sdk_folder_id"]
        if "smart_contract_address" in body["data"]:
            modification["smart_contract_address"] = body["data"]["smart_contract_address"]

        await database.update_dapp(user_id=user_id,
                                   dapp_id=dapp_id,
                                   modification=modification,
                                   unset=unset)

async def handle_rollback_update_dapp_event(body, reply_to, message_id, database):
    _LOGGER.debug("Receiving response about dapp rollback updating process")

    if 'error' in body:
        user_id = body["error"]["user_id"]
        dapp_id = body["error"]["dapp_id"]

        dapps = await database.get_dapps(dapp_id=dapp_id, user_id=user_id)
        dapp = dapps[0]
        modification = {
            "diagrams": dapp["temp_diagrams"],
            "entities": dapp["temp_entities"],
            "dapp_description": dapp["temp_dapp_description"],
            "dapp_logo": dapp["temp_dapp_logo"],
            "temp_diagrams": dapp["diagrams"],
            "temp_entities": dapp["entities"],
            "temp_dapp_description": dapp["dapp_description"],
            "temp_dapp_logo": dapp["dapp_logo"],
            "status": DappStatus.UPDATE_FAIL.name,
            "message": body["error"]["message"]
        }

        await database.update_dapp(user_id=user_id,
                                   dapp_id=dapp_id,
                                   modification=modification)
    else:
        user_id = body["data"]["user_id"]
        dapp_id = body["data"]["dapp_id"]
        
        modification = {
            "status": DappStatus.CREATED.name,
            "dapp_version": body["data"]["dapp_version"]
        }

        unset = {
            "temp_entities": "",
            "temp_diagrams": "",
            "temp_dapp_description": "",
            "temp_dapp_logo": "",
            "message": ""
        }
            

        if "sdk_folder_id" in body["data"]:
            modification["sdk_folder_id"] = body["data"]["sdk_folder_id"]

        await database.update_dapp(user_id=user_id,
                                   dapp_id=dapp_id,
                                   modification=modification,
                                   unset=unset)

async def handle_delete_dapp_event(body, reply_to, message_id, database):
    _LOGGER.debug("Receiving response about dapp deleting process")
    
    if 'error' in body:
        user_id = body["error"]["user_id"]
        dapp_id = body["error"]["dapp_id"]
        await database.update_dapp(user_id=user_id,
                                   dapp_id=dapp_id,
                                   modification={"status": DappStatus.DELETE_FAIL.name,
                                                 "message": body["error"]["message"]})
    else:
        user_id = body["data"]["user_id"]
        dapp_id = body["data"]["dapp_id"]
        await database.delete_dapp(user_id=user_id, dapp_id=dapp_id)
