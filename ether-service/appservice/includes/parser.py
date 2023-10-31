import os
import sys
import copy

import elasticsearch_client as elastic

print(os.getcwd())
sys.path.append("..")

mapping_default_type_proto = {
    "string": "string",
    "uuid": "string",
    "int": "sint64",
    "file": "string",
    "img": "img",
    "image": "img",
}
mapping_type_method = {"UPDATE": "PUT", "GET": "GET", "CREATE": "POST"}


def parser_property(object_property, object_level, parent_object_name):
    if object_property["type"] != "object":
        property_temp = {
            "name": object_property["name"],
            "description": object_property["description"],
            "type": object_property["type"],
            "proto_type": mapping_default_type_proto[object_property["type"]],
        }

        prefix_name = ""
        if parent_object_name != "" or object_level != 1:
            prefix_name = parent_object_name + "__"

        if object_property["type"] == 'file':
            property_temp["proto_name"] = prefix_name + object_property["name"] + "_cid"
            property_temp["db_name"] = prefix_name + object_property["name"] + "_cid"

        else:
            property_temp["proto_name"] = prefix_name + object_property["name"]
            property_temp["db_name"] = prefix_name + object_property["name"]

    else:
        property_temp = {
            "name": object_property["name"],
            "description": object_property["description"],
            "type": object_property["type"],
            "properties": [],
        }
        if parent_object_name == "" and object_level == 1:
            parent_object_name = object_property["name"]
        else:
            parent_object_name = parent_object_name + "__" + object_property["name"]
        for object_property_child in object_property["child"]:
            property_temp["properties"].append(
                parser_property(
                    object_property=object_property_child, 
                    object_level=object_level+1, 
                    parent_object_name=parent_object_name))

    return property_temp


def flatten_parameters(parameters_info):
    flat_parameters = []
    print("PARA INFO: {}".format(parameters_info))

    def flatten(child_info, parent_name):
        for child in child_info:
            child["name"] = parent_name + "." + child["name"]
            if child["type"] != "object":
                flat_parameters.append({
                    "name": child["name"],
                    "type": child["type"],
                    "proto_type": child["proto_type"],
                    "proto_name": child["proto_name"],
                    "db_name": child["db_name"]
                })
            else:
                flatten(child["properties"], child["name"])

    for parameter in parameters_info:
        if parameter["type"] != "object":
            flat_parameters.append({
                "name": parameter["name"],
                "type": parameter["type"],
                "proto_type": parameter["proto_type"],
                "proto_name": parameter["proto_name"],
                "db_name": parameter["db_name"]
            })
        else:
            flatten(parameter["properties"], parameter["name"])

    print("FLAT: {}".format(flat_parameters))
    return flat_parameters


async def parse_configuration(
        nameDirModule, nameModule, description, methods, assets, roles, uuids, enable_trace
):
    res = elastic.get_version_applications(nameModule)
    applications = res["hits"]["hits"]
    if len(applications) == 0:
        version_module = 1.0
    else:
        version_module = applications[0]["_source"]["version_module"] + 0.1
        applications[0]["_source"]["version_module"] = version_module
    body = {"application_name": nameModule, "version_module": version_module}
    elastic.create_version_applications_record(body)

    basic_info = {
        "nameDirModule": nameDirModule,
        "author": "BKC",
        "author_email": "hust.blockchain@gmail.com",
        "project_name": nameModule,
        "version_module": version_module,
        "docs": {"openapi": {"title": nameModule + "REST API"}},
        "module_name": nameModule,
        "api_description": description,
    }

    properties = []
    for object_property in assets:
        property_temp = parser_property(object_property=object_property, object_level=1, parent_object_name="")
        properties.append(property_temp)

    for method in methods:
        method["http_method"] = mapping_type_method[method["type"]]
        method["params_detail"] = []
        method["uuids"] = []
        for param_name in method["params"]:
            for proper in properties:
                if param_name == proper["name"]:
                    if param_name in uuids:
                        method["uuids"].append(proper)
                    method['params_detail'].append(proper)

        method["flat_params"] = flatten_parameters(copy.deepcopy(method["params_detail"]))
        flat_properties = flatten_parameters(copy.deepcopy(properties))

    dapp_configuration = {
        "basic_info": basic_info,
        "properties": properties,
        "flat_properties": flat_properties,
        "methods": methods,
        "roles": roles,
        "uuids": uuids,
        "enable_trace": enable_trace,
    }

    return dapp_configuration

