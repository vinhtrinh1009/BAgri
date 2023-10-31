from jsonschema import validate, FormatChecker

network_config_schema = {
    "type": "object",
    "properties": {
        "network_id": {"type": "string"},
        "name": {"type": "string", "pattern": "^[a-z][a-z0-9-]{0,49}$"},
        # "blockchain_type": {"type": "string", "pattern": "^[Ff][Aa][Bb][Rr][Ii][Cc]$"},
        # "consensus": {
        #     "type": "string",
        #     "pattern": "^[Pp][Bb][Ff][Tt]$|^[Rr][Aa][Ff][Tt]$",
        # },
        "node_infrastructure": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "pattern": "^internal$"},
                "number_vm_nodes": {"type": "string", "pattern": "^[1-9][0-9]{0,1}$"},
                "node_plan": {
                    "type": "object",
                    "properties": {
                        "cpu": {"type": "number"},
                        "ram": {"type": "number"},
                        "disk": {"type": "number"},
                    },
                    "required": [
                        "cpu",
                        "ram",
                        "disk",
                    ],
                },
            },
            "required": [
                "type",
                "number_vm_nodes",
                "node_plan",
            ],
        },
        "blockchain_peer_config": {
            "type": "object",
            "properties": {
                "organizations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "pattern": "^[a-z][a-z0-9]{0,49}$",
                                "not": {"enum":["orderer"]}
                            },
                            "number_peer": {
                                "type": "number",
                                "minimum": 1,
                                "maximum": 99,
                            },
                        },
                        "required": ["name", "number_peer"],
                    },
                    "minItems": 1,
                    "maxItems": 20,
                }
            },
            "required": ["organizations"],
        },
    },
    "required": [
        "name",
        # "blockchain_type",
        # "consensus",
        "node_infrastructure",
        "blockchain_peer_config",
        "network_id",
    ],
}

network_update_info_schema = {
    "type": "object",
    "properties": {
        "update_type": {
            "type": "string",
        },
        "config": {},
    },
    "required": [
        "update_type",
        "config",
    ],
}

resource_config_schema = {
    "type": "object",
    "properties": {
        "resource_id": {"type": "string"},
        "resource_name": {"type": "string"},
        "resource_description": {"type": "string"},
        "resource_config": {
            "type": "object",
            "properties": {
                "organization_name": {
                    "type": "string",
                    "pattern": "^[a-z][a-z0-9-]{0,49}$",
                },
                "host": {
                    "type": "string",
                    "format": "ipv4",
                },
                "port": {
                    "anyOf": [
                        {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 65535,
                        },
                        {
                            "type": "string",
                            "pattern": "^[1-9][0-9]{0,4}$"
                        }
                    ]
                },
            },
            "required": ["organization_name", "host", "port"],
        },
    },
    "required": [
        "resource_id",
        "resource_name",
        "resource_description",
        "resource_config",
    ],
}

# try:
#     instance = {
#         "resource_id": "alo",
#         "resource_name": "test",
#         "resource_config": {
#             "organization_name": "hust",
#             "host": "143.198.84.186.99.99",
#             "port": 7054,
#         },
#         "resource_description": "test",
#     }

#     validate(
#         instance=instance, schema=resource_config_schema, format_checker=FormatChecker()
#     )
# except Exception as e:
#     print(e.message)
#     print(e.relative_schema_path)
