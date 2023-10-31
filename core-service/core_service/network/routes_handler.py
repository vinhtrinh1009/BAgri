import copy
from importlib import resources
import json
import resource

from utils.logging import get_logger
from utils.response import success, ApiBadRequest, ApiInternalError
from network.status import NetworkStatus
from network.status import ResourceStatus
from dapp.status import DappStatus

_LOGGER = get_logger(__name__)


class NetworkHandler:
    def __init__(self, database, broker_client):
        self.__database = database
        self.__broker_client = broker_client
        self.__supported_platform = ["sawtooth", "fabric", "ethereum"]

    async def create_network(self, user_info, new_network):
        if new_network["blockchain_type"] in self.__supported_platform:
            network_id = await self.__database.create_network({
                "name": new_network["name"],
                "blockchain_type": new_network["blockchain_type"],
                "consensus": new_network["consensus"],
                "node_infrastructure": new_network["node_infrastructure"],
                "blockchain_peer_config": new_network["blockchain_peer_config"],
                "user_id": user_info["user_id"],
                "status": NetworkStatus.CREATE_PENDING.name
            })

            routing_key = f"driver.{new_network['blockchain_type']}.request.create_network"
            message = {
                "network_info": {
                    "network_id": network_id,
                    "name": new_network["name"],
                    "blockchain_type": new_network["blockchain_type"],
                    "consensus": new_network["consensus"],
                    "node_infrastructure": new_network["node_infrastructure"],
                    "blockchain_peer_config": new_network["blockchain_peer_config"],
                    "status": NetworkStatus.CREATE_PENDING.name
                },
                "user_info": {
                    "username": user_info["username"],
                    "user_id": user_info["user_id"]
                }
            }
            await self.__broker_client.publish(routing_key=routing_key,
                                               message=json.dumps(message),
                                               reply_to="coreservice.events.create_network")
            # try catch if cannot request
            # -> delete the record and raise ApiInternalError("cannot create a network")
            # else return {network_id, status}
            return success({
                "network_id": network_id,
                "status": NetworkStatus.CREATE_PENDING.name
            })
        else:
            raise ApiBadRequest("The system does not support {}".format(new_network["blockchain_type"]))

    async def retry_create_network(self, user_info, network_id):
        user_id = user_info["user_id"]
        if not await self.is_create_failed_network(network_id=network_id):
            raise ApiBadRequest("Cannot retry create network unless the network was failed to create")

        modification = {
            "status": NetworkStatus.CREATE_PENDING.name
        }
        network = await self.__database.update_network(user_id=user_id,
                                                       network_id=network_id,
                                                       modification=modification)

        if network["network_id"] is not None:
            if network["blockchain_type"] in self.__supported_platform:
                routing_key = f"driver.{network['blockchain_type']}.request.retry_create_network"
                message = {
                    "network_info": {
                        "network_id": network["network_id"],
                        "name": network["name"],
                        "blockchain_type": network["blockchain_type"],
                        "consensus": network["consensus"],
                        "node_infrastructure": network["node_infrastructure"],
                        "blockchain_peer_config": network["blockchain_peer_config"],
                        "status": NetworkStatus.CREATE_PENDING.name
                    },
                    "user_info": {
                        "username": user_info["username"],
                        "user_id": user_info["user_id"]
                    }
                }
                await self.__broker_client.publish(routing_key=routing_key,
                                                   message=json.dumps(message),
                                                   reply_to="coreservice.events.create_network")
                return success({
                    "network_id": network_id,
                    "status": NetworkStatus.CREATE_PENDING.name
                })
        else:
            raise ApiInternalError("Cannot change status of the network")

    async def update_network(self, user_info, network_id, update_info):
        user_id = user_info["user_id"]

        network_pending, network = await self.is_pending_network(network_id=network_id)

        if network_pending:
            raise ApiBadRequest("Cannot update network at this time because the network is pending")

        # modification = {
        #     "status": NetworkStatus.UPDATE_PENDING.name
        # }
        # network = await self.__database.update_network(user_id=user_id,
        #                                                network_id=network_id,
        #                                                modification=modification)
        if network["network_id"] is not None:
            if network["blockchain_type"] == "fabric":
                dapps = await self.__database.get_dapps(network_id=network["network_id"])
                for dapp in dapps:
                    if "PENDING" in dapp["status"]:
                        raise ApiBadRequest(f"Cannot update network at this time because the dapp {dapp['dapp_id']} is pending")

                modification = {
                    "status": NetworkStatus.UPDATE_PENDING.name
                }
                await self.__database.update_network(user_id=user_id,
                                                    network_id=network["network_id"],
                                                    modification=modification)

                routing_key = f"driver.{network['blockchain_type']}.request.update_network"
                message = {
                    "update_info": update_info,
                    "network_id": network_id,
                    "user_info": {
                        "username": user_info["username"],
                        "user_id": user_info["user_id"]
                    }
                }
                _LOGGER.debug(f"PUBLISH UPDATE NETWORK MESSAGE: {message}")
                await self.__broker_client.publish(routing_key=routing_key,
                                                    message=json.dumps(message),
                                                    reply_to="coreservice.events.update_network")
                return success({
                    "network_id": network_id,
                    "status": NetworkStatus.UPDATE_PENDING.name
                })

            else:
                raise ApiBadRequest("The system does not support {}".format(network["blockchain_type"]))
        else:
            raise ApiInternalError("Cannot change status of the network")
    
    async def retry_update_network(self, user_info, network_id):
        user_id = user_info["user_id"]

        update_fail, network = await self.is_update_failed_network(network_id=network_id)

        if not update_fail:
            raise ApiBadRequest("Can only retry update failed network")

        if network["network_id"] is not None:
            dapps = await self.__database.get_dapps(network_id=network["network_id"])
            for dapp in dapps:
                if "PENDING" in dapp["status"]:
                    raise ApiBadRequest(f"Cannot update network at this time because the dapp {dapp['dapp_id']} is pending")

            if network["blockchain_type"] == "fabric":
                modification = {
                    "status": NetworkStatus.UPDATE_PENDING.name
                }
                await self.__database.update_network(user_id=user_id,
                                                    network_id=network["network_id"],
                                                    modification=modification)
                routing_key = f"driver.{network['blockchain_type']}.request.retry_update_network"
                message = {
                    "network_id": network_id,
                    "user_info": {
                        "username": user_info["username"],
                        "user_id": user_info["user_id"]
                    }
                }
                _LOGGER.debug(f"PUBLISH UPDATE NETWORK MESSAGE: {message}")
                await self.__broker_client.publish(routing_key=routing_key,
                                                    message=json.dumps(message),
                                                    reply_to="coreservice.events.update_network")
                return success({
                    "network_id": network_id,
                    "status": NetworkStatus.UPDATE_PENDING.name
                })

            else:
                raise ApiBadRequest("The system does not support {}".format(network["blockchain_type"]))
        else:
            raise ApiInternalError("Cannot change status of the network")

    async def rollback_update_network(self, user_info, network_id):
        user_id = user_info["user_id"]

        update_fail, network = await self.is_update_failed_network(network_id=network_id)

        if not update_fail:
            raise ApiBadRequest("Can only rollback update failed network")

        if network["network_id"] is not None:
            dapps = await self.__database.get_dapps(network_id=network["network_id"])
            for dapp in dapps:
                if "PENDING" in dapp["status"]:
                    raise ApiBadRequest(f"Cannot update network at this time because the dapp {dapp['dapp_id']} is pending")

            if network["blockchain_type"] == "fabric":
                modification = {
                    "status": NetworkStatus.UPDATE_PENDING.name
                }
                await self.__database.update_network(user_id=user_id,
                                                    network_id=network["network_id"],
                                                    modification=modification)
                routing_key = f"driver.{network['blockchain_type']}.request.rollback_update_network"
                message = {
                    "network_id": network_id,
                    "user_info": {
                        "username": user_info["username"],
                        "user_id": user_info["user_id"]
                    }
                }
                _LOGGER.debug(f"PUBLISH UPDATE NETWORK MESSAGE: {message}")
                await self.__broker_client.publish(routing_key=routing_key,
                                                    message=json.dumps(message),
                                                    reply_to="coreservice.events.update_network")
                return success({
                    "network_id": network_id,
                    "status": NetworkStatus.UPDATE_PENDING.name
                })

            else:
                raise ApiBadRequest("The system does not support {}".format(network["blockchain_type"]))
        else:
            raise ApiInternalError("Cannot change status of the network")


    async def get_network(self, user_id, network_id):
        networks = await self.__database.get_networks(network_id=network_id, user_id=user_id)
        for network in networks:
            dapps = await self.__database.get_dapps(network_id=network["network_id"])
            network["dapps"] = dapps
        return success(networks)

    async def get_user_networks(self, user_info):
        networks = await self.__database.get_networks(user_id=user_info["user_id"])
        
        # For ethereum network
        external_networks = [
            {
                "code": "bsc",
                "name": "BSC Mainnet"
            },
            {
                "code": "bsct",
                "name": "BSC Testnet"
            },
            {
                "code": "ftm",
                "name": "Fantom Mainnet"
            },
            {
                "code": "ftmt",
                "name": "Fantom Testnet"
            },
            {
                "code": "rinkeby",
                "name": "Rinkeby Testnet"
            },
            {
                "code": "ropsten",
                "name": "Ropsten Testnet"
            }
        ]
        for external_network in external_networks:
            if any(network["node_infrastructure"]["type"] == 'external' and network["node_infrastructure"]["name"] == external_network["code"] for network in networks):
                pass
            else:
                new_network = {
                    "name": external_network["name"],
                    "blockchain_type": "ethereum",
                    "consensus": "pow",
                    "node_infrastructure": {
                        "type": "external",
                        "name": external_network["code"]
                    },
                    "blockchain_peer_config": {}
                }
                await self.create_network(user_info, new_network)
        return success(networks)

    async def delete_network(self, user_info, network_id):
        user_id = user_info["user_id"]
        network_pending, network = await self.is_pending_network(network_id=network_id)
        if network_pending:
            raise ApiBadRequest("Cannot delete network at this time because the network is pending")

        # modification = {
        #     "status": NetworkStatus.DELETE_PENDING.name
        # }
        # network = await self.__database.update_network(user_id=user_id,
        #                                                network_id=network_id,
        #                                                modification=modification)


        if network["network_id"] is not None:
            dapps = await self.__database.get_dapps(network_id=network["network_id"])
            for dapp in dapps:
                if "PENDING" in dapp["status"]:
                    raise ApiBadRequest(f"Cannot delete network at this time because the dapp {dapp['dapp_name']} is pending")
                # await self.__database.update_dapp(dapp["dapp_id"], user_id, {"status": DappStatus.DELETE_PENDING.name})

            modification = {
                "status": NetworkStatus.DELETE_PENDING.name
            }
            await self.__database.update_network(user_id=user_id,
                                                network_id=network["network_id"],
                                                modification=modification)
            
            await self.__database.update_multi_dapp(network["network_id"], user_id, {"status": DappStatus.DELETE_PENDING.name})        

            if network["blockchain_type"] in self.__supported_platform:
                routing_key = f"driver.{network['blockchain_type']}.request.delete_network"
                message = {
                    "network_info": {
                        "network_id": network["network_id"],
                        "name": network["name"],
                        "status": NetworkStatus.DELETE_PENDING.name
                    },
                    "user_info": {
                        "username": user_info["username"],
                        "user_id": user_info["user_id"]
                    },
                    "dapps": dapps
                }
                _LOGGER.debug(f"PUBLISH DELETE NETWORK MESSAGE: {message}")
                await self.__broker_client.publish(routing_key=routing_key,
                                                   message=json.dumps(message),
                                                   reply_to="coreservice.events.delete_network")
                return success({
                    "network_id": network_id,
                    "status": NetworkStatus.DELETE_PENDING.name
                })
        else:
            raise ApiInternalError("Cannot change status of the network")

    async def create_resource(self, user_info, network_id, new_resource):
        _LOGGER.info(new_resource)
        networks = await self.__database.get_networks(network_id=network_id,
                                                      user_id=user_info["user_id"])

        if len(networks) > 1:
            raise ApiInternalError(f"Have more than one network with network_id: {network_id}")
        elif len(networks) == 0:
            raise ApiInternalError(f"Don't have network with network_id: {network_id}")
        network = networks[0]

        if "PENDING" in network["status"]:
            raise ApiInternalError(f"Cannot create resource because network {network['name']} is pending")

        dapps = await self.__database.get_dapps(network_id=network["network_id"])
        for dapp in dapps:
            if await self.is_pending_dapp(dapp_id=dapp["dapp_id"]):
                raise ApiBadRequest(f"Cannot delete network at this time because the dapp {dapp['dapp_id']} is pending")
        
        resource_id = await self.__database.create_resource({
            "resource_name": new_resource["resource_name"],
            "resource_description": new_resource["resource_description"],            
            "network_id": network_id,
            "user_id": user_info["user_id"],
            "resource_config": new_resource["resource_config"],
            "status": ResourceStatus.CREATE_PENDING.name
        })

        routing_key = f"driver.{network['blockchain_type']}.request.create_resource"
        
        new_resource["resource_id"] = resource_id

        message = {
            "resource_info": new_resource,
            "network_id": network_id,
            "user_info": {
                "username": user_info["username"],
                "user_id": user_info["user_id"]
            }
        }
        _LOGGER.debug(routing_key)
        await self.__broker_client.publish(routing_key=routing_key,
                                           message=json.dumps(message),
                                           reply_to="coreservice.events.create_resource")
        return success({
            "resource_id": resource_id,
            "status": ResourceStatus.CREATE_PENDING.name
        })

    async def get_network_resources(self, network_id):
        resources = await self.__database.get_resources(network_id=network_id)
        return success(resources)
    
    async def is_pending_network(self, network_id):
        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ApiInternalError("More than one network have the same network_id")
        elif len(networks) == 0:
            raise ApiInternalError("Network does not exist")
        network = networks[0]
        return "PENDING" in network["status"], network

    async def is_pending_dapp(self, dapp_id):
        dapps = await self.__database.get_dapps(dapp_id=dapp_id)
        if len(dapps) > 1:
            raise ApiInternalError("More than one dapp have the same dapp_id")
        elif len(dapps) == 0:
            raise ApiInternalError("Dapp does not exist")
        dapp = dapps[0]
        return "PENDING" in dapp["status"]

    async def is_create_failed_network(self, network_id):
        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ApiInternalError("More than one network have the same network_id")
        elif len(networks) == 0:
            raise ApiInternalError("Network does not exist")
        network = networks[0]
        return "CREATE_FAIL" in network["status"]

    async def is_update_failed_network(self, network_id):
        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ApiInternalError("More than one network have the same network_id")
        elif len(networks) == 0:
            raise ApiInternalError("Network does not exist")
        network = networks[0]
        return "UPDATE_FAIL" in network["status"], network
