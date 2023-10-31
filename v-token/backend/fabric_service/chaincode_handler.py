import os
from fabric_service.database import Database
from bson.objectid import ObjectId
from fabric_service.const import BASE_DIR
from fabric_service.exceptions import ThirdPartyRequestError, ServiceError
from fabric_service.generate_chaincode import generate_chaincode_file
from fabric_service.generate_mint_script import generate_mint_file
from fabric_service.generate_burn_file import generate_burn_file
from fabric_service.logging_config import get_logger
from fabric_service.k8s import get_public_ip
from fabric_service.generate_sdk import generate_sdk
_LOGGER = get_logger(__name__)

class ChaincodeHandler:
    def __init__(self, db_host, db_port, db_name, db_username, db_password, k8s_token):
        self.__database = Database(db_host, db_port, db_username, db_password, db_name)
        self.__k8s = k8s_token
    
    async def ConnectDB(self):
        await self.__database.connect()
    
    async def get_dapps(self, user_id):
        response = await self.__database.get_dapps(user_id=user_id)
        return response
    
    async def get_networks(self, user_id):
        response = await self.__database.get_networks(user_id=user_id)
        return response

    async def handler_create_chaincode(self, chaincode_config, network_id, user_info):
        chaincode_config['token_name']=chaincode_config['token_name'].replace(" ", "")
        new_dapp = {}
        new_dapp['dapp_name'] = chaincode_config['token_name']
        new_dapp['entities'] = {}
        new_dapp['entities']['token_standard'] = chaincode_config['token_standard'],
        new_dapp['entities']['token_symbol'] = chaincode_config['token_symbol'], 
        new_dapp['entities']['decimal'] = chaincode_config['decimal'],
        new_dapp['entities']['initial_supply'] = chaincode_config['initial_supply']
        new_dapp['network_id'] = network_id
        
        # return chaincode_config['network_id']
        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {new_dapp['network_id']}"
            )
        elif len(networks) == 0:
            raise ServiceError(
                f"Don't have network with network_id: {new_dapp['network_id']}"
            )
        
        network_config = networks[0]
        nodeIp =get_public_ip(cluster_id=network_config["cluster_id"], digital_ocean_token=self.__k8s)
        # return network_config
        print(network_config)
        print(nodeIp)
        new_dapp['dapp_version']=1
        dapp_folder = os.path.join(
                BASE_DIR,
                "projects",
                user_info['username'],
                network_config["network_id"],
                "dapps",
                new_dapp['dapp_name'],
            )
        
        if not os.path.exists(dapp_folder):
            _LOGGER.debug(f"Create folder: {dapp_folder}")
            os.makedirs(dapp_folder)

        kube_config_path = os.path.join(
            BASE_DIR,
            "projects",
            user_info['username'],
            network_config["network_id"],
            "k8s_config.yaml",
        )
        chaincode_id = await self.__database.create_dapp({
                "_id": ObjectId(oid=None),
                "dapp_name": new_dapp["dapp_name"],
                "dapp_description": "",
                "dapp_version": new_dapp["dapp_version"],
                "entities": new_dapp["entities"],
                "network_id": new_dapp["network_id"],
                "dapp_folder_id": "",
                "user_id": user_info['user_id'],
                "sdk_key": "",
            })
        response = await generate_chaincode_file(
            chaincode_config=chaincode_config,
            network_config=network_config,
            chaincode_folder=dapp_folder,
            user_info= user_info,
            kube_config_path=kube_config_path,
            chaincode_version=new_dapp["dapp_version"],
            nodeIp=nodeIp
        )

        return response
    
    async def handler_invoke_chaincode_mint(self, token_name, network_id, user_info, quantity, minter_org, minter_username):
        token_name=token_name.replace(" ", "")
        
        # return chaincode_config['network_id']
        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {network_id}"
            )
        elif len(networks) == 0:
            raise ServiceError(
                f"Don't have network with network_id: {network_id}"
            )
        
        network_config = networks[0]
        nodeIp =get_public_ip(cluster_id=network_config["cluster_id"], digital_ocean_token=self.__k8s)
        # return network_config
        print(network_config)
        print(nodeIp)

        response = await generate_mint_file(
            chaincode_config=token_name,
            network_config=network_config,
            user_info= user_info,
            nodeIp=nodeIp,
            quantity=quantity,
            minter_org=minter_org,
            minter_username=minter_username
        )

        return response

    async def handler_invoke_chaincode_burn(self, token_name, network_id, user_info, quantity, to_address, to_token):
        token_name=token_name.replace(" ", "")
        
        # return chaincode_config['network_id']
        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {network_id}"
            )
        elif len(networks) == 0:
            raise ServiceError(
                f"Don't have network with network_id: {network_id}"
            )
        
        network_config = networks[0]
        nodeIp =get_public_ip(cluster_id=network_config["cluster_id"], digital_ocean_token=self.__k8s)
        # return network_config
        print(network_config)
        print(nodeIp)
        
        response = await generate_burn_file(
            chaincode_config=token_name,
            network_config=network_config,
            user_info= user_info,
            nodeIp=nodeIp,
            quantity=quantity,
            to_address=to_address,
            token_address=to_token
        )

        return response
    
    async def handler_generate_sdk(self, token_name, network_id, user_info):
        token_name=token_name.replace(" ", "")
        
        # return chaincode_config['network_id']
        networks = await self.__database.get_networks(network_id=network_id)
        if len(networks) > 1:
            raise ServiceError(
                f"Have more than one network with network_id: {network_id}"
            )
        elif len(networks) == 0:
            raise ServiceError(
                f"Don't have network with network_id: {network_id}"
            )
        network = networks[0]

        response = await generate_sdk(token_name, user_info, network_id, network)
        return response



