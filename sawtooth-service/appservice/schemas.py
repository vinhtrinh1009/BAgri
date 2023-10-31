from jsonschema import validate, FormatChecker

network_config_schema = {
    "type": "object",
    "properties": {
        "network_id": {"type": "string"},
        "name": {"type": "string", "pattern": "^[a-z][a-z0-9-]{0,49}$"},
        # "blockchain_type": {"type": "string", "pattern": "^[Ff][Aa][Bb][Rr][Ii][Cc]$"},
        "consensus": {
            "type": "string",
            # "pattern": "^[Pp][Bb][Ff][Tt]$|^[Rr][Aa][Ff][Tt]$",
        },
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
                "number_peer": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 99,
                },
            },                
            "required": ["number_peer"],
        },
    },
    "required": [
        "name",
        "consensus",
        "node_infrastructure",
        "blockchain_peer_config",
        "network_id",
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
                "host": {
                    "type": "string",
                    "format": "ipv4",
                },
                "port": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 65535,
                },
            },
            "required": ["host", "port"],
        },
    },
    "required": [
        "resource_id",
        "resource_name",
        "resource_description",
        "resource_config",
    ],
}