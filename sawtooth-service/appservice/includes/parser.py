from attr import attributes
from config.logging_config import get_logger
from generator import proto_generator, sdk_generator, processor_generator, addressing_generator, docs_generator
from exceptions import SchemaError

_LOGGER = get_logger(__name__)

mapping_default_type_proto = {
    "string": "string",
    "uuid": "string",
    "int": "int",
    "file": "string",
    "img": "img",
    "image": "img",
    "array": "array"
}

mapping_type_method = {"UPDATE": "PUT", "GET": "GET", "CREATE": "POST"}


async def parse_entities(entities, parsed_relationships):
    try:    
        parsed_entities = []
        # add new attribute due to relationship between entities
        for index, entity in enumerate(entities):
            has_encrypt = False
            parsed_attributes = []
            mapping_att = {
                "container":"1",
                "state_entries":"1",
                "data":"1",
                "updated_state":"1",
                "_context":"1",
                "_timeout":"1"
            }
            if entity["primary_key"] in mapping_att:
                temp = entity['name'] + entity['primary_key']
                entity["primary_key"]=temp
            # parse attributes added by user on UI
            for attribute in entity["attributes"]:
                if attribute["encrypt"]:
                    has_encrypt = True
                mapping_att[attribute["name"]+"_address"] = "1"
                if attribute["name"] == "timestamp" or attribute["name"] == "encrypt_data":
                    raise SchemaError(f"attribute cannot be named timestamp or encrypt_data")
                if attribute["name"] in mapping_att:
                    temp = entity["name"]+ "_" + attribute["name"]
                    attribute["name"]=temp
                mapping_att[attribute["name"]] = "1"     
                parsed_attributes.append({
                    "name": attribute["name"],
                    "type": attribute["type"],
                    "proto_name": attribute["name"],
                    "proto_type": mapping_default_type_proto[attribute["type"]],
                    "relationship_att": False,
                    "encrypt": attribute["encrypt"]
                })

            # parse to get new attribute from relationships
            for relationship in parsed_relationships:
                if relationship["source_entity"] == entity["name"]:
                    reference_entity_primary_attribute = await get_primary_attribute(entities=entities,
                                                                                    entity_name=relationship["reference_entity"])
                    new_attribute_name = relationship["reference_entity"] + "_" + reference_entity_primary_attribute["name"]
                    if new_attribute_name in mapping_att:
                        temp = "for_" + new_attribute_name
                        new_attribute_name = temp
                    if relationship["reference_type"] == "N":

                        parsed_attributes.append({
                            "name": new_attribute_name + "s",
                            "type": "array",
                            "proto_name": new_attribute_name + "s",
                            "proto_type": mapping_default_type_proto["array"],
                            "relationship_att": True,
                            "encrypt" : False
                        })
                    elif relationship["reference_type"] == "1":

                        parsed_attributes.append({
                            "name": new_attribute_name,
                            "type": "string",
                            "proto_name": new_attribute_name,
                            "proto_type": mapping_default_type_proto["string"],
                            "relationship_att": True,
                            "encrypt" : False
                        })
            parsed_entities.append({
                "name": entity["name"],
                "attributes": parsed_attributes,
                "address_prefix": index,
                "primary_key": entity["primary_key"],
                "has_encrypt": has_encrypt
            })

        return parsed_entities

    except Exception:
        raise SchemaError("ERROR entities, attribute cannot be named timestamp or encrypt_data")


async def get_primary_attribute(entities, entity_name):
    for entity in entities:
        if entity["name"] == entity_name:
            primary_key = entity["primary_key"]
            primary_attribute = await get_attribute_by_name(entity, primary_key)
            return primary_attribute


async def get_attribute_by_name(entity, name):
    for attribute in entity["attributes"]:
        if attribute["name"] == name:
            return attribute


async def parse_relationship(entities):
    try:    
        _relationships = []

        for _entity in entities:
            if "relationships" in _entity:
                _LOGGER.debug(f"entity: {_entity}")
                for relationship in _entity["relationships"]:
                    if relationship["type"] == "1:N" or relationship["type"] == "1:n":
                        _relationships.append({
                            "source_entity": _entity["name"],
                            "source_type": "1",
                            "reference_entity": relationship["reference_to_entity"],
                            "reference_type": "N"
                        })
                        _relationships.append({
                            "source_entity": relationship["reference_to_entity"],
                            "source_type": "1",
                            "reference_entity": _entity["name"],
                            "reference_type": "1"
                        })
                    elif relationship["type"] == "N:1":
                        _relationships.append({
                            "source_entity": _entity["name"],
                            "source_type": "1",
                            "reference_entity": relationship["reference_to_entity"],
                            "reference_type": "1"
                        })
                        _relationships.append({
                            "source_entity": relationship["reference_to_entity"],
                            "source_type": "1",
                            "reference_entity": _entity["name"],
                            "reference_type": "N"
                        })
                    elif relationship["type"] == "1:1":
                        _relationships.append({
                            "source_entity": _entity["name"],
                            "source_type": "1",
                            "reference_entity": relationship["reference_to_entity"],
                            "reference_type": "1"
                        })
                        _relationships.append({
                            "source_entity": relationship["reference_to_entity"],
                            "source_type": "1",
                            "reference_entity": _entity["name"],
                            "reference_type": "1"
                        })
                    elif relationship["type"] == "N:N" or relationship["type"] == "n:n":
                        _relationships.append({
                            "source_entity": _entity["name"],
                            "source_type": "1",
                            "reference_entity": relationship["reference_to_entity"],
                            "reference_type": "N"
                        })
                        _relationships.append({
                            "source_entity": relationship["reference_to_entity"],
                            "source_type": "1",
                            "reference_entity": _entity["name"],
                            "reference_type": "N"
                        })

        return _relationships
    except Exception:
        raise SchemaError(f"Fail gen relationship")


async def parse_functions(parsed_entities):
    try: 
        parsed_functions = {
            "get_functions": [],
            "create_functions": [],
            "update_functions": []
        }
        for entity in parsed_entities:
            # function for creating the entity
            parsed_functions["create_functions"].append({
                "name": f"create_{entity['name']}",
                "type": "CREATE",
                "params": [{"name": _att['name'],
                            "type": _att['type'],
                            "proto_name": _att["proto_name"],
                            "proto_type": _att["proto_type"],
                            "encrypt": _att['encrypt']}
                        for _att in entity["attributes"]],
                "action_name": f"Create{entity['name'].capitalize()}Action",
                "required_fields": [entity['primary_key']],
                "http_method": "POST",
                "api_name": f"create_{entity['name']}",
                "entity_name": entity["name"],
                "entity_primary_key": entity["primary_key"],
                "has_encrypt" : entity["has_encrypt"]
            })

            # function for updating the entity
            parsed_functions["update_functions"].append({
                "name": f"update_{entity['name']}",
                "type": "UPDATE",
                "params": [{"name": _att['name'],
                            "type": _att['type'],
                            "proto_name": _att["proto_name"],
                            "proto_type": _att["proto_type"],
                            "encrypt": _att['encrypt']}
                        for _att in entity["attributes"]],
                "action_name": f"Update{entity['name'].capitalize()}Action",
                "required_fields": [entity['primary_key']],
                "http_method": "PUT",
                "api_name": f"update_{entity['name']}",
                "entity_name": entity["name"],
                "entity_primary_key": entity["primary_key"],
                "has_encrypt" : entity["has_encrypt"]
            })

            # function for getting the entity
            parsed_functions["get_functions"].append({
                "name": f"get_{entity['name']}",
                "type": "GET",
                "params": [{"name": _att['name'],
                            "type": _att['type'],
                            "proto_name": _att["proto_name"],
                            "proto_type": _att["proto_type"],
                            "encrypt": _att['encrypt']}
                        for _att in entity["attributes"]],
                "http_method": "GET",
                "api_name": f"get_{entity['name']}",
                "entity_name": entity["name"],
                "entity_primary_key": entity["primary_key"],
                "has_encrypt" : entity["has_encrypt"]
            })

        return parsed_functions
    except Exception:
        raise SchemaError(f"Fail gen function")

async def parse_protobufs(parsed_entities, old_protobufs):
    try:
        for entity in parsed_entities:
            new_protobufs = []
            new_attributes = []
            temp = 0
            check = await find_element(old_protobufs, entity["name"])
            if check == -1 :
                for index, att in enumerate(entity["attributes"]):
                    if att["encrypt"] == False:
                        new_attributes.append({
                            "name" : att["name"],
                            "proto_name": att["name"],
                            "proto_type": mapping_default_type_proto[att["type"]],
                            "indexOf" : index + 1 - temp,
                        })
                    else:
                        temp = temp + 1
                if temp > 0:                
                    new_attributes.append({
                        "name": "encrypt_data",
                        "proto_name": "encrypt_data",
                        "proto_type": "string",
                        "indexOf" : len(new_attributes) + temp,
                    })
                new_protobufs.append({
                    "name" : entity["name"],
                    "attributes": new_attributes
                })
                old_protobufs.extend(new_protobufs)
            else: 
                for index, att in enumerate(entity["attributes"]):
                    att_index = await find_element(old_protobufs[check]["attributes"], att["name"]) 
                    if (att["encrypt"] == False) and (att_index == -1): 
                        temp = len(old_protobufs[check]["attributes"])        
                        old_protobufs[check]["attributes"].append({
                            "name": att["name"],
                            "proto_name": att["name"],
                            "proto_type": mapping_default_type_proto[att["type"]],
                            "indexOf": 1 + temp,
                        })
                    elif att["encrypt"] == True:
                        att_index = await find_element(old_protobufs[check]["attributes"], "encrypt_data")
                        if att_index == -1:
                            temp = len(old_protobufs[check]["attributes"])  
                            old_protobufs[check]["attributes"].append({
                                "name": "encrypt_data",
                                "proto_name": "encrypt_data",
                                "proto_type": "string",
                                "indexOf": 1 + temp,
                            })
        return old_protobufs
    except Exception:
        raise SchemaError(f"Fail gen protobuf")
            

async def find_element(array, name):
    if len(array) == 0:
        return -1
    else:
        for i, element in enumerate(array):
            if element["name"] == name:
                return i
        return -1
                
async def gen_code(dapp_info, user_info, number_peer, public_ip, dst_folder="application"):
    try:
        _LOGGER.debug(f"dapp info : {dapp_info}")
        parsed_relationships = await parse_relationship(dapp_info["entities"])
        _LOGGER.debug(f"====parsed relationship: {parsed_relationships}")

        parsed_entities = await parse_entities(entities=dapp_info["entities"],
                                            parsed_relationships=parsed_relationships)
        _LOGGER.debug(f"=====parsed entities: {parsed_entities}")

        parsed_functions = await parse_functions(parsed_entities)
        _LOGGER.debug(f"=====parsed functions: {parsed_functions}")

        parse_protobuf = await parse_protobufs(parsed_entities, dapp_info["old_protobufs"])

        data_rendering = {
            "entities": parsed_entities,
            "protobufs": parse_protobuf,
            "functions": parsed_functions,
            "relationships": parsed_relationships,
            'basic_info': {
                'dapp_name': dapp_info['dapp_name'],
                'dapp_id' : dapp_info['dapp_id'],
                'dapp_description': dapp_info['dapp_description'],
                'number_peer': number_peer,
                'public_ip': public_ip,
                'dapp_version': dapp_info['dapp_version'],
                'username': user_info['username'],
                'dapp_folder_id': dapp_info['dapp_folder_id'],
                'sdk_key' : dapp_info['sdk_key'],
                'data_folder_id': dapp_info['data_folder_id'],
                'encryptionType': dapp_info['encryption_type'].upper()
            }
        }

        proto_generator.gen_code(data=data_rendering, dst_folder=dst_folder)
        addressing_generator.gen_code(data=data_rendering, dst_folder=dst_folder)
        processor_generator.gen_code(data=data_rendering, dst_folder=dst_folder)
        sdk_generator.gen_code(data=data_rendering, dst_folder=dst_folder)
        docs_generator.gen_docs(data=data_rendering)
        _LOGGER.debug(f"Generated all file of dapp: {dapp_info['dapp_name']}")
        return parse_protobuf
    except Exception:
        raise SchemaError("Fail gen code")
