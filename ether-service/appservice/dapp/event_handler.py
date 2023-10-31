import os
import yaml
import time
import copy
import json
from generator import smart_contract_generator
from config.logging_config import get_logger
from worker.tasks import git_delete_group
import settings
import constants

_LOGGER = get_logger(__name__)


class DappHandler:
    def __init__(self, database, broker_client):
        self.__database = database
        self.__broker_client = broker_client

    async def handle_create_dapp(self, body, reply_to, message_id):
        dapp_info = body["dapp_info"]
        user_info = body["user_info"]

        _LOGGER.debug(f"Receive a request to create a dapp with dapp_id: {dapp_info['network_id']}")
        dapp_user_folder = f"Applications/{user_info['username']}"
        is_update = False
        await gen_code(dapp_info=dapp_info,user_info=user_info, dapp_user_folder=dapp_user_folder, is_update=is_update, reply_to=reply_to)

        # push_to_git(dapp_info, user_info, dapp_user_folder, is_update, reply_to)

        # await self.__broker_client.publish(routing_key=reply_to, message=json.dumps(success_message), reply_to=reply_to)
    
    async def handle_update_dapp(self, body, reply_to, message_id):
        dapp_info = body["dapp_info"]
        user_info = body["user_info"]

        _LOGGER.debug(f"Receive a request to update a dapp with dapp_id: {dapp_info['network_id']}")
        dapp_user_folder = f"Applications/{user_info['username']}"
        is_update = True
        await gen_code(dapp_info=dapp_info,user_info=user_info, dapp_user_folder=dapp_user_folder, is_update=is_update, reply_to=reply_to)


    async def handle_delete_dapp(self, body, reply_to, message_id):
        dapp_info = body["dapp_info"]
        user_info = body["user_info"]
        _LOGGER.debug(f"Receive a request to delete dapp with dapp_id: {dapp_info['network_id']}")
        await git_delete_group.delay(dapp_info, user_info, reply_to)

        dapp_path = os.path.join(base_dir, f"Applications/{user_info['username']}")
        os.chdir(dapp_path)
        cmd(
            f'rm -rf {dapp_info["dapp_name"]} {dapp_info["dapp_name"]}_sdk'
        )
        os.sys(cmd)



async def gen_code(dapp_info, user_info, dapp_user_folder, is_update, reply_to):

    # Initiate data rendering
    data_rendering = {
        'basic_info': {
            'dapp_name': dapp_info['dapp_name'],
            'dapp_description': dapp_info['dapp_description'],
            'network_id': dapp_info['network_id'],
            'version_module': 1.0
        },
        'entities': [],
        'user_info': user_info
    }

    for i, _entity in enumerate(dapp_info['entities']):
        # Basic information
        _entity_name = _entity['name']
        attributes = []
        for _attribute in _entity['attributes']:
            if _attribute['name'] == _entity['primary_key']:
                _primary_key_type = _attribute['type']
            
            if _attribute['type'] == 'file' or _attribute['type'] == 'object':
                attributes.append({
                    'name': _attribute['name'],
                    'type': 'string'
                })
            else:
                attributes.append({
                    'name': _attribute['name'],
                    'type': _attribute['type']
                })

        _entity_information = {
            'name': _entity_name,
            'attributes': attributes,
            'primary_key': _entity['primary_key'],
            'primary_key_type': _primary_key_type
        }

        
        
        # Extract relationship information
        relationship = []
        if 'relationship' in _entity:
            for _relationship in _entity['relationship']:
                referenced_entity = _relationship['reference_to_entity']
                relationship_type = _relationship['type']
                for _reference_entity in dapp_info['entities']:

                    if _reference_entity['name'] == referenced_entity:
                        _reference_entity_primary_key = _reference_entity['primary_key']
                        for _attribute in _reference_entity['attributes']:
                            
                            if _attribute['name'] == _reference_entity_primary_key:
                                
                                if _attribute['type'] == 'file' or _attribute['type'] == 'object':
                                    _reference_entity_primary_type = 'string'
                                else:
                                    _reference_entity_primary_type = _attribute['type']

                _relationship_infor = {
                    'referenced_entity': referenced_entity,
                    'relationship_type': relationship_type,
                    '_reference_entity_primary_key': _reference_entity_primary_key,
                    '_reference_entity_primary_type': _reference_entity_primary_type
                }
                relationship.append(_relationship_infor)
        _entity_information['relationship'] = relationship

        # Extract function information
        _create_function = {
            'type': 'CREATE',
            'name': f'create{_entity_name.capitalize()}',
            'python_name': f'create_{_entity_name}',
            'params': attributes
        }
        _get_function = {
            'type': 'GET',
            'name': f'get{_entity_name.capitalize()}',
            'python_name': f'get_{_entity_name}',
        }
        # _update_method = {
        #     'name': f'update_{_entity_name.capitalize()}'
        # }
        _entity_information['functions'] = [_get_function, _create_function]

        data_rendering['entities'].append(_entity_information)

    # generate smart contract
    contract_address = smart_contract_generator.gen_code(data_rendering, dapp_user_folder, dapp_info, user_info, is_update, reply_to)





# def push_to_git(dapp_info, user_info, project_path, project_name, is_update, reply_to):
#     if is_update:
#         git_push_without_create.delay(user_info["username"],
#                                       sdk_path,
#                                       smart_contract_path,
#                                       "update dapp")
#     else:
#         git_push.delay(dapp_info=dapp_info,
#                     user_info=user_info,
#                     project_path=project_path,
#                     project_name=project_name,
#                     commit_message="Create DApp",
#                     reply_to=reply_to)

