import pathlib
import os
import yaml
import sys
import copy

print(os.getcwd())
sys.path.append("..")


def create_swagger_schema(properties):

    schema = {}
    for proper in properties:
        if proper["type"] == "object":
            swagger_property = {
                proper["name"]: {
                    "type": "object",
                    "properties": {}
                }
            }
            child_properties = proper["properties"]
            swagger_property[proper["name"]]["properties"] = create_swagger_schema(child_properties)

        elif proper["type"] == "file":
            swagger_property = {
                proper["name"]+"_cid": {
                    "type": "string"
                }
            }
        else:
            swagger_property = {
                proper["name"]: {
                    "type": proper["type"]
                }
            }
        schema.update(swagger_property)
    return schema


def flatten_parameters(parameters_info):
    flat_parameters = []
    print("PARA INFO: {}".format(parameters_info))

    def flatten(child_info, parent_name):
        for child in child_info:
            child["name"] = parent_name + "." + child["name"]
            if child["type"] != "object":
                flat_parameters.append(child)
            else:
                flatten(child["properties"], child["name"])

    for parameter in parameters_info:
        if parameter["type"] != "object":
            flat_parameters.append(parameter)
        else:
            flatten(parameter["properties"], parameter["name"])
    print("FLAT: {}".format(flat_parameters))
    return flat_parameters


def parse_parameters(parameters_info, position):
    # type: FORMDATA, QUERY, BODY
    parameters = []
    if position == "BODY":
        schema = create_swagger_schema(parameters_info)
        parameters.append({
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": schema
            }
        })
    else:
        flat_parameters = flatten_parameters(parameters_info)
        for parameter in flat_parameters:
            if position == "QUERY":
                if parameter["type"] == "file":
                    parameter["type"] = "string"
                    parameter["name"] = parameter["name"] + "_cid"
                parameters.append({
                    "name": parameter["name"],
                    "type": parameter["type"],
                    "in": "query",
                    "required": True
                })
            elif position == "FORMDATA":
                parameters.append({
                    "name": parameter["name"],
                    "type": parameter["type"],
                    "in": "formData",
                    "required": True
                })
    return parameters


async def generate_swagger(dapp_configuration):
    swagger = {
        "host": "188.166.199.221/apps/api/"
                + str(dapp_configuration["basic_info"]["module_name"]),
        "basePath": "/",
        "swagger": "2.0",
        "schemes": ["http"],
    }

    info = {
        "version": "1.0.0",
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
        },
        "contact": {
            "email": dapp_configuration["basic_info"]["author_email"]
        },
        "title": dapp_configuration["basic_info"]["module_name"] + " API",
        "description": dapp_configuration["basic_info"]["module_name"] + " API",
    }
    swagger["info"] = info

    tags = []
    user_role_description = "Roles : "
    for role in dapp_configuration["roles"]:
        tag_temp = {"name": role, "description": role}
        user_role_description = user_role_description + role.upper() + " "
        tags.append(tag_temp)
    swagger["tags"] = tags

    swagger["paths"] = {}
    for method in dapp_configuration["methods"]:
        swagger_method = {
            "produces": ["application/json"],
            "responses": {
                "200": {},
                "400": {"description": "Invalid Syntax"},
                "500": {"description": "Internal Server Error"},
            },
        }

        method_params_detail = []
        uuid_params_detail = []
        for param in method["params"]:
            for proper in dapp_configuration["properties"]:
                if param == proper["name"]:
                    if method["type"] == "CREATE" and param in dapp_configuration["uuids"]:
                        uuid_params_detail.append(proper)
                    else:
                        method_params_detail.append(proper)
                    break

        params = []
        if method["type"] != "GET":
            if method["contentType"] == "multipart/form-data":
                swagger_method["consumes"] = ["multipart/form-data"]
                params = parse_parameters(copy.deepcopy(method_params_detail), position="FORMDATA")
            else:
                swagger_method["consumes"] = ["application/json"]
                params = parse_parameters(copy.deepcopy(method_params_detail), position="BODY")

        else:
            params = parse_parameters(copy.deepcopy(method_params_detail), position="QUERY")

        swagger_method["parameters"] = params

        response_200 = {}
        if method["type"] == "GET":
            response_200 = {
                "description": "OK",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": create_swagger_schema(dapp_configuration["properties"])}
                }
            }
        elif method["type"] == "CREATE":
            response_200 = {
                "description": "OK",
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string"
                        }
                    }
                }
            }
            for uuid in uuid_params_detail:
                response_200["schema"]["properties"][uuid["name"]] = {
                    "type": uuid["type"]
                }
        elif method["type"] == "UPDATE":
            response_200 = {
                "description": "OK",
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string"
                        }
                    }
                }
            }
        swagger_method["responses"]["200"] = response_200

        swagger_method["tags"] = method["roles"]

        swagger["paths"]["/" + method["name"]] = {}

        swagger["paths"]["/" + method["name"]][method["http_method"].lower()] = swagger_method

    default_paths = {
        "/user": {
            "post": {
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "user",
                        "description": user_role_description,
                        "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["username", "password", "role"],
                            "properties": {
                                "username": {"type": "string"},
                                "password": {"type": "string"},
                                "role": {"type": "string"},
                            },
                        },
                    }
                ],
                "responses": {
                    "200": {"description": "created"},
                    "400": {"description": "username exist"},
                },
                "tags": ["default"]
            }
        },
        "/authentication": {
            "post": {
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "tags": ["default"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "default",
                        "description": "default",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["username", "password"],
                            "properties": {
                                "username": {"type": "string"},
                                "password": {"type": "string"},
                            },
                        },
                    }
                ],
                "responses": {
                    "200": {
                        "description": "login success",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "status": {
                                    "type": "string",
                                    "enum": ["Success", "Failure"],
                                },
                                "authorization": {
                                    "type": "string",
                                    "enum": [
                                        "eyJleHAiOjE1NjExMDQyMDIsImFsZyI6IkhTNTEyIiwiaWF0IjoxNTYxMTAwNjAyfQ.eyJwdWJsaWNfa2V5IjoiMDM3YTRhZTliZWYwMDhkZGY3YjUwODE0N2ZlNjc0OTFhYmMzZWEyNzkyZmYxMjY0MDgwODAwZTJmODg2Nzc2MGJlIn0.LreIkJoa6Ha1sZXTBN8i_smrDPmCRMu0cGzXjs9qH2Aj9IkHh9iXNj-pT-nYW8f_SNYdkpHR1lxMqpVasvNhqA",
                                        "Incorrect username or password",
                                        "Missing required fields",
                                    ],
                                },
                            },
                        },
                    }
                },
            }
        }
    }

    swagger["paths"].update(default_paths)
    print("SWAGGER_RETURN: {}".format(swagger))

    return swagger
