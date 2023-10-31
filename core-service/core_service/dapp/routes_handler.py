import json
import os

from aiohttp import web
from utils.logging import get_logger
from utils.response import success, ApiBadRequest, ApiInternalError
from dapp.status import DappStatus

_LOGGER = get_logger(__name__)


class DappHandler:
    def __init__(self, database, broker_client):
        self.__database = database
        self.__broker_client = broker_client

    async def create_dapp(self, user_info, new_dapp):
        _LOGGER.info(new_dapp)
        dapp_id = await self.__database.create_dapp({
            "dapp_name": new_dapp["dapp_name"],
            "dapp_description": new_dapp["dapp_description"],
            "dapp_version": 1,
            "dapp_logo": new_dapp["dapp_logo"],
            "encryption_type": new_dapp["encryption_type"],
            "entities": new_dapp["entities"],
            "network_id": new_dapp["network_id"],
            "user_id": user_info["user_id"],
            "diagrams": new_dapp["diagrams"],
            "status": DappStatus.CREATE_PENDING.name
        })

        networks = await self.__database.get_networks(network_id=new_dapp["network_id"],
                                                          user_id=user_info["user_id"])
        if len(networks) > 1:
            raise ApiInternalError(f"Have more than one network with network_id: {new_dapp['network_id']}")
        elif len(networks) == 0:
            raise ApiInternalError(f"Don't have network with network_id: {new_dapp['network_id']}")

        network = networks[0]
        if "PENDING" in network["status"]:
            raise ApiInternalError(f"Cannot create dapp because network {network['name']} is pending")
        routing_key = f"driver.{network['blockchain_type']}.request.create_dapp"
        
        message = {
            "dapp_info": {
                "dapp_id": dapp_id,
                "dapp_name": new_dapp["dapp_name"],
                "dapp_description": new_dapp["dapp_description"],
                "dapp_version": 1,
                "encryption_type": new_dapp["encryption_type"],
                "entities": new_dapp["entities"],
                "network_id": new_dapp["network_id"],
                "status": DappStatus.CREATE_PENDING.name
            },
            "user_info": {
                "username": user_info["username"],
                "user_id": user_info["user_id"]
            }
        }
        _LOGGER.debug(routing_key)
        await self.__broker_client.publish(routing_key=routing_key,
                                           message=json.dumps(message),
                                           reply_to="coreservice.events.create_dapp")
        return success({
            "dapp_id": dapp_id,
            "status": DappStatus.CREATE_PENDING.name
        })

    async def retry_create_dapp(self, user_info, dapp_id):
        _LOGGER.info(dapp_id)

        dapps = await self.__database.get_dapps(dapp_id=dapp_id, user_id=user_info["user_id"])
    
        if len(dapps) > 1:
            raise ApiInternalError(f"Have more than one dapp with dapp_id: {dapp_id}")
        elif len(dapps) == 0:
            raise ApiInternalError(f"Don't have dapp with dapp_id: {dapp_id}")

        dapp = dapps[0]

        if not "CREATE_FAIL" in dapp["status"]:
            raise ApiInternalError(f"Cannot retry create dapp unless dapp was failed to create")

        networks = await self.__database.get_networks(network_id=dapp["network_id"],
                                                          user_id=user_info["user_id"])

        if len(networks) > 1:
            raise ApiInternalError(f"Have more than one network with network_id: {dapp['network_id']}")
        elif len(networks) == 0:
            raise ApiInternalError(f"Don't have network with network_id: {dapp['network_id']}")

        network = networks[0]
        if "PENDING" in network["status"]:
            raise ApiInternalError(f"Cannot create dapp because network {network['name']} is pending")

        modification = {
            "status": DappStatus.CREATE_PENDING.name
        }
        await self.__database.update_dapp(dapp_id, user_info["user_id"], modification)
        
        routing_key = f"driver.{network['blockchain_type']}.request.retry_create_dapp"
        
        message = {
            "dapp_info": {
                "dapp_id": dapp_id,
                "dapp_name": dapp["dapp_name"],
                "dapp_description": dapp["dapp_description"],
                "dapp_version": 1,
                "encryption_type": dapp["encryption_type"],
                "entities": dapp["entities"],
                "network_id": dapp["network_id"],
                "status": DappStatus.CREATE_PENDING.name
            },
            "user_info": {
                "username": user_info["username"],
                "user_id": user_info["user_id"]
            }
        }
        _LOGGER.debug(routing_key)
        await self.__broker_client.publish(routing_key=routing_key,
                                           message=json.dumps(message),
                                           reply_to="coreservice.events.create_dapp")
        return success({
            "dapp_id": dapp_id,
            "status": DappStatus.CREATE_PENDING.name
        })

    async def update_dapp(self, dapp_id, user_info, update_dapp):
        dapps = await self.__database.get_dapps(dapp_id=dapp_id, user_id=user_info["user_id"])

        if len(dapps) > 1:
            raise ApiInternalError(f"Have more than one dapp with dapp_id: {dapp_id}")
        elif len(dapps) == 0:
            raise ApiInternalError(f"Don't have dapp with dapp_id: {dapp_id}")

        dapp = dapps[0]
        if "PENDING" in dapp["status"] or "FAIL" in dapp["status"]:
            raise ApiInternalError(f"Cannot update dapp because dapp {dapp_id} is not ready")
        
        networks = await self.__database.get_networks(network_id=dapp["network_id"],
                                                          user_id=user_info["user_id"])

        if len(networks) > 1:
            raise ApiInternalError(f"Have more than one network with network_id: {dapp['network_id']}")
        elif len(networks) == 0:
            raise ApiInternalError(f"Don't have network with network_id: {dapp['network_id']}")

        network = networks[0]
        if "PENDING" in network["status"]:
            raise ApiInternalError(f"Cannot update dapp because network {network['name']} is pending")

        if dapp["entities"] == update_dapp["entities"]:
            modification = {
                "diagrams": update_dapp["diagrams"],
                "dapp_logo": update_dapp["dapp_logo"],
                "dapp_description": update_dapp["dapp_description"]
            }
            await self.__database.update_dapp(dapp_id, user_info["user_id"], modification)
            
            return success({
                "dapp_id": dapp_id,
                "status": DappStatus.CREATED.name
            })
        else:
            modification = {
                "dapp_logo": update_dapp["dapp_logo"],
                "entities": update_dapp["entities"],
                "diagrams": update_dapp["diagrams"],
                "status": DappStatus.UPDATE_PENDING.name,
                "temp_dapp_logo": dapp["dapp_logo"],
                "temp_entities": dapp["entities"],
                "temp_diagrams": dapp["diagrams"],
                "temp_dapp_description": dapp["dapp_description"],
                "dapp_description": update_dapp["dapp_description"]
            }
            await self.__database.update_dapp(dapp_id, user_info["user_id"], modification)

            # networks = await self.__database.get_networks(network_id=update_dapp["network_id"],
            #                                                 user_id=user_info["user_id"])
            # if len(networks) > 1:
            #     raise ApiInternalError(f"Have more than one network with network_id: {update_dapp['network_id']}")
            # elif len(networks) == 0:
            #     raise ApiInternalError(f"Don't have network with network_id: {update_dapp['network_id']}")

            # network = networks[0]
            # if "PENDING" in network["status"]:
            #     raise ApiInternalError(f"Cannot update dapp because network {network['name']} is pending")
            routing_key = f"driver.{network['blockchain_type']}.request.update_dapp"

            message = {
                "dapp_info": {
                    "dapp_id": dapp_id,
                    "dapp_name": dapp["dapp_name"],
                    "dapp_description": update_dapp["dapp_description"],
                    "dapp_version": dapp["dapp_version"] + 1,
                    "encryption_type": dapp["encryption_type"],
                    "entities": update_dapp["entities"],
                    "network_id": dapp["network_id"],
                    "status": DappStatus.UPDATE_PENDING.name
                },
                "user_info": {
                    "username": user_info["username"],
                    "user_id": user_info["user_id"]
                }
            }
            await self.__broker_client.publish(routing_key=routing_key,
                                            message=json.dumps(message),
                                            reply_to="coreservice.events.update_dapp")

            return success({
                "dapp_id": dapp_id,
                "status": DappStatus.UPDATE_PENDING.name
            })

    async def retry_update_dapp(self, user_info, dapp_id):
        dapps = await self.__database.get_dapps(dapp_id=dapp_id, user_id=user_info["user_id"])
    
        if len(dapps) > 1:
            raise ApiInternalError(f"Have more than one dapp with dapp_id: {dapp_id}")
        elif len(dapps) == 0:
            raise ApiInternalError(f"Don't have dapp with dapp_id: {dapp_id}")

        dapp = dapps[0]

        if not "UPDATE_FAIL" in dapp["status"]:
            raise ApiInternalError(f"Cannot retry update dapp unless dapp was failed to update")

        networks = await self.__database.get_networks(network_id=dapp["network_id"],
                                                          user_id=user_info["user_id"])

        if len(networks) > 1:
            raise ApiInternalError(f"Have more than one network with network_id: {dapp['network_id']}")
        elif len(networks) == 0:
            raise ApiInternalError(f"Don't have network with network_id: {dapp['network_id']}")

        network = networks[0]
        if "PENDING" in network["status"]:
            raise ApiInternalError(f"Cannot update dapp because network {network['name']} is pending")

        modification = {
            "status": DappStatus.UPDATE_PENDING.name
        }
        await self.__database.update_dapp(dapp_id, user_info["user_id"], modification)
        
        routing_key = f"driver.{network['blockchain_type']}.request.retry_update_dapp"
        
        message = {
            "dapp_info": {
                "dapp_id": dapp_id,
                "dapp_name": dapp["dapp_name"],
                "dapp_description": dapp["dapp_description"],
                "dapp_version": dapp["dapp_version"] + 1,
                "encryption_type": dapp["encryption_type"],
                "entities": dapp["entities"],
                "network_id": dapp["network_id"],
                "status": DappStatus.UPDATE_PENDING.name
            },
            "user_info": {
                "username": user_info["username"],
                "user_id": user_info["user_id"]
            }
        }
        _LOGGER.debug(message)
        await self.__broker_client.publish(routing_key=routing_key,
                                           message=json.dumps(message),
                                           reply_to="coreservice.events.update_dapp")
        return success({
            "dapp_id": dapp_id,
            "status": DappStatus.UPDATE_PENDING.name
        })

    async def rollback_update_dapp(self, user_info, dapp_id):
        dapps = await self.__database.get_dapps(dapp_id=dapp_id, user_id=user_info["user_id"])
    
        if len(dapps) > 1:
            raise ApiInternalError(f"Have more than one dapp with dapp_id: {dapp_id}")
        elif len(dapps) == 0:
            raise ApiInternalError(f"Don't have dapp with dapp_id: {dapp_id}")

        dapp = dapps[0]
        if not "UPDATE_FAIL" in dapp["status"]:
            raise ApiInternalError(f"Cannot retry update dapp unless dapp was failed to update")

        networks = await self.__database.get_networks(network_id=dapp["network_id"],
                                                          user_id=user_info["user_id"])

        if len(networks) > 1:
            raise ApiInternalError(f"Have more than one network with network_id: {dapp['network_id']}")
        elif len(networks) == 0:
            raise ApiInternalError(f"Don't have network with network_id: {dapp['network_id']}")

        network = networks[0]
        if "PENDING" in network["status"]:
            raise ApiInternalError(f"Cannot update dapp because network {network['name']} is pending")

        modification = {
            "diagrams": dapp["temp_diagrams"],
            "entities": dapp["temp_entities"],
            "dapp_description": dapp["temp_dapp_description"],
            "temp_diagrams": dapp["diagrams"],
            "temp_entities": dapp["entities"],
            "temp_dapp_description": dapp["dapp_description"],
            "status": DappStatus.UPDATE_PENDING.name
        }
        await self.__database.update_dapp(dapp_id, user_info["user_id"], modification)

        routing_key = f"driver.{network['blockchain_type']}.request.rollback_update_dapp"
        
        message = {
            "dapp_info": {
                "dapp_id": dapp_id,
                "dapp_name": dapp["dapp_name"],
                "dapp_description": dapp["dapp_description"],
                "dapp_version": dapp["dapp_version"],
                "encryption_type": dapp["encryption_type"],
                "entities": dapp["entities"],
                "network_id": dapp["network_id"],
                "status": DappStatus.UPDATE_PENDING.name
            },
            "user_info": {
                "username": user_info["username"],
                "user_id": user_info["user_id"]
            }
        }
        _LOGGER.debug(message)
        await self.__broker_client.publish(routing_key=routing_key,
                                           message=json.dumps(message),
                                           reply_to="coreservice.events.rollback_update_dapp")
        return success({
            "dapp_id": dapp_id,
            "status": DappStatus.UPDATE_PENDING.name
        })

    async def delete_dapp(self, user_info, dapp_id):
        user_id = user_info["user_id"]
        if await self.is_pending_dapp(dapp_id=dapp_id):
            raise ApiBadRequest("Cannot delete dapp at this time")

        modification = {
            "status": DappStatus.DELETE_PENDING.name
        }
        dapp = await self.__database.update_dapp(user_id=user_id,
                                                 dapp_id=dapp_id,
                                                 modification=modification)

        networks = await self.__database.get_networks(network_id=dapp["network_id"],
                                                      user_id=user_info["user_id"])

        network = networks[0]
        if len(networks) > 1:
            raise ApiInternalError(f"Have more than one network with network_id: {dapp['network_id']}")

        if dapp["dapp_id"] is not None:
            routing_key = f"driver.{network['blockchain_type']}.request.delete_dapp"
            message = {
                "dapp_info": {
                    "dapp_name": dapp["dapp_name"],
                    "network_id": network["network_id"],
                    "dapp_id": dapp["dapp_id"],
                    "dapp_version": dapp["dapp_version"],
                    "status": DappStatus.DELETE_PENDING.name
                },
                "user_info": {
                    "username": user_info["username"],
                    "user_id": user_info["user_id"]
                }
            }
            await self.__broker_client.publish(routing_key=routing_key,
                                               message=json.dumps(message),
                                               reply_to="coreservice.events.delete_dapp")
            return success({
                "dapp_id": dapp_id,
                "status": DappStatus.DELETE_PENDING.name
            })

    async def retry_delete_dapp(self, user_info, dapp_id):
        user_id = user_info["user_id"]
        if await self.is_pending_dapp(dapp_id=dapp_id):
            raise ApiBadRequest("Cannot retry delete dapp at this time")

        modification = {
            "status": DappStatus.DELETE_PENDING.name
        }
        dapp = await self.__database.update_dapp(user_id=user_id,
                                                 dapp_id=dapp_id,
                                                 modification=modification)
                                                 
        networks = await self.__database.get_networks(network_id=dapp["network_id"],
                                                      user_id=user_info["user_id"])

        network = networks[0]
        if len(networks) > 1:
            raise ApiInternalError(f"Have more than one network with network_id: {dapp['network_id']}")

        if dapp["dapp_id"] is not None:
            routing_key = f"driver.{network['blockchain_type']}.request.retry_delete_dapp"
            message = {
                "dapp_info": {
                    "dapp_name": dapp["dapp_name"],
                    "network_id": network["network_id"],
                    "dapp_id": dapp["dapp_id"],
                    "dapp_version": dapp["dapp_version"],
                    "status": DappStatus.DELETE_PENDING.name
                },
                "user_info": {
                    "username": user_info["username"],
                    "user_id": user_info["user_id"]
                }
            }
            await self.__broker_client.publish(routing_key=routing_key,
                                               message=json.dumps(message),
                                               reply_to="coreservice.events.delete_dapp")
            return success({
                "dapp_id": dapp_id,
                "status": DappStatus.DELETE_PENDING.name
            })

    async def get_dapp(self, user_id, dapp_id):
        dapps = await self.__database.get_dapps(dapp_id=dapp_id, user_id=user_id)
        return success(dapps)

    async def get_dapp_by_sdk_key(self, sdk_key):
        dapps = await self.__database.get_dapps(sdk_key=sdk_key)
        return success(dapps)

    async def get_user_dapps(self, user_id):
        dapps = await self.__database.get_dapps(user_id=user_id)
        return success(dapps)

    async def is_pending_dapp(self, dapp_id):
        dapps = await self.__database.get_dapps(dapp_id=dapp_id)
        if len(dapps) > 1:
            raise ApiInternalError(f"More than one dapp have the same dapp_id: {dapp_id}")
        elif len(dapps) == 0:
            raise ApiInternalError(f"Don't have dapp with the id: {dapp_id}")
        dapp = dapps[0]
        return "PENDING" in dapp["status"]
