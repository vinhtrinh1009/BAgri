import requests

from settings import config

from constants import BASE_DIR
from includes import utils
from config.logging_config import get_logger
from exceptions import DocsServiceRequestError

_LOGGER = get_logger(__name__)

def gen_docs(data):
    try:    
        dapp_info = {
            "dapp_id": data['basic_info']['dapp_id'],
            "dapp_name": data['basic_info']['dapp_name'],
            "dapp_description": data['basic_info']['dapp_description'],
            "username": data['basic_info']['username']
        }

        # add folder tree-----------------------------------
        folder_tree = {
        "folder_tree": [
            {
            "name": "address",
            "children": [
                {
                "name": "address.py",
                "description": "address"
                }
            ]
            },
            {
            "name": "handler.py",
            "description": "Package"
            },
            {
            "name": "transaction_creation.py",
            "description": "encode payload, make batch."
            },
            {
            "name": "error.py",
            "description": "Error"
            },
            {
            "name": "messaging.py",
            "description": "connect validator, sign transaction"
            }
        ]
        }

        protobuf = {
            "name": "protobuf",
            "children": [
                {
                "name": "protobuf.py",
                "description": "Enroll Admin file."
                }
            ]
        }

        for entity in data['entities']:
            temp = { "name": entity['name'] + ".py", 
            "description": "encode " + entity['name'] + "." }
            protobuf["children"].append(temp)

        folder_tree["folder_tree"].append(protobuf)

        dapp_info.update(folder_tree)
        # ----------------end folder tree------------------------------
        # add getting started------------------------------------------
        getting_started = {
        "getting_started": [
            {
            "instruction": "Install requirement package",
            "description": "Open Terminal, change directory to SDK folder and run below command",
            "commands": [
                {
                "language": "bash",
                "command": "pip install -r requirements.txt"
                }
            ]
            },
            {
            "instruction": "Import SDK",
            "commands": [
                {
                "language": "python",
                "command": "import handler"
                }
            ]
            },
            {
            "instruction": "Development with function in SDK"
            }
        ]
        }

        dapp_info.update(getting_started)
        # ----------------end getting_started------------------------------
        # start function---------------------------------------------------
        functions = {"functions": [
            {
                "name": "trace",
                "description": "get transaction",
                "parameters": [
                    {
                        "name": "transaction_ids",
                        "type": "string",
                        "description": "transaction id"
                    }
                ],
                "returns": {
                    "type": "json",
                    "description": "transaction info",
                    "fields": [
                        {
                            "name": "result",
                            "type": "object",
                            "description": "transaction info"
                        }
                    ]
                }
            },
            {
                "name": "gen_key_pair",
                "description": "gen public, private key",
                "parameters": [],
                "returns": {
                    "type": "string",
                    "description": "public, private key",
                    "fields": [
                        {
                            "name": "public key",
                            "type": "string",
                            "description": "public key"
                        },
                        {
                            "name": "private key",
                            "type": "string",
                            "description": "private key"
                        }
                    ]
                }
            }
        ]}
        for function in (data['functions']['create_functions'] + data['functions']['update_functions']):
            temp_function = {"name" : function['name'],
                "description": function['name'],
                "parameters": [{
                        "name": "private_key",
                        "type": "string",
                        "description": "private key"
                    }
                ],
                "returns": {
                    "type": "json",
                    "description": function['name'],
                    "fields": [
                        {
                            "name": "txid",
                            "type": "string",
                            "description": "transaction id"
                        }
                    ]
                } 
            }
            for param in function['params']:
                temp_param = {"name" : param['name'], "type": param['type']}
                temp_function["parameters"].append(temp_param)        
            functions["functions"].append(temp_function)
        
        for function in data['functions']['get_functions']:
            temp_function = {"name" : function['name'],
                "description": function['name'],
                "parameters": [{
                        "name": function['entity_primary_key'],
                        "type": "string",
                        "description": function['entity_primary_key']
                    }
                ],
                "returns": {
                    "type": "json",
                    "description": function['name'],
                    "fields": [
                        {
                            "name": function['entity_name'],
                            "type": "json",
                            "description": function['entity_name']
                        }
                    ]
                } 
            }        
            functions["functions"].append(temp_function)
        
        dapp_info.update(functions)
        schema = {
                "$defs": {
                    "folder_tree_component": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "children": {
                                "type": "array",
                                "items": {"$ref": "#/$defs/folder_tree_component"},
                            },
                        },
                        "required": ["name"],
                    },
                    "command_component": {
                        "type": "object",
                        "properties": {
                            "language": {"type": "string"},
                            "command": {"type": "string"},
                        },
                        "required": ["command"],
                    },
                    "getting_started_component": {
                        "type": "object",
                        "properties": {
                            "instruction": {"type": "string"},
                            "description": {"type": "string"},
                            "commands": {
                                "type": "array",
                                "items": {"$ref": "#/$defs/command_component"},
                            },
                        },
                        "required": ["instruction"],
                    },
                    "object_component": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "description": {"type": "string"},
                            "fields": {
                                "type": "array",
                                "items": {"$ref": "#/$defs/object_component"},
                            },
                        },
                        "required": ["name", "type"],
                    },
                    "return_component": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "description": {"type": "string"},
                            "fields": {
                                "type": "array",
                                "items": {"$ref": "#/$defs/object_component"},
                            },
                        },
                        "required": ["type"],
                    },
                    "function_component": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "parameters": {
                                "type": "array",
                                "items": {"$ref": "#/$defs/object_component"},
                            },
                            "returns": {"$ref": "#/$defs/return_component"},
                        },
                        "required": ["name", "parameters", "returns"],
                    },
                },
                "type": "object",
                "properties": {
                    "dapp_id": {"type": "string"},
                    "dapp_name": {"type": "string"},
                    "username": {"type": "string"},
                    "dapp_description": {"type": "string"},
                    "folder_tree": {
                        "type": "array",
                        "items": {"$ref": "#/$defs/folder_tree_component"},
                    },
                    "getting_started": {
                        "type": "array",
                        "items": {"$ref": "#/$defs/getting_started_component"},
                    },
                    "functions": {
                        "type": "array",
                        "items": {"$ref": "#/$defs/function_component"},
                    },
                },
                "required": [
                    "dapp_id",
                    "dapp_name",
                    "username",
                    "folder_tree",
                    "getting_started",
                    "functions",
                ],
            }

        url = config["docs_service"]["host"]

        
        response = requests.post(url, json = dapp_info)

        _LOGGER.debug(f"====GEN DOCS: {response}")
    except Exception as e:
        raise DocsServiceRequestError("Fail to create document")
