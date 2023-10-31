import copy
from exceptions import SchemaError
from utils import schemas
from jsonschema import validate


def update_network_config(old_network_config, update_info):

    network_config = None

    if update_info["update_type"] == "new_organization":
        network_config = new_organization(old_network_config, update_info["config"])

    else:
        raise SchemaError("Invalid Update Type")

    validate(instance=network_config, schema=schemas.network_config_schema)
    return network_config


def new_organization(old_network_config, config):
    network_config = copy.deepcopy(old_network_config)
    organizations = network_config["blockchain_peer_config"]["organizations"]
    config_schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "pattern": "^[a-z][a-z0-9-]{0,49}$",
            },
            "number_peer": {
                "type": "number",
                "minimum": 1,
                "maximum": 9,
            },
        },
        "required": ["name", "number_peer"],
    }

    validate(instance=config, schema=config_schema)

    names = []

    for org in organizations:
        names.append(org["name"])

    if config["name"] in names:
        raise SchemaError("Duplicated organization name")

    organizations.append(config)

    return network_config
