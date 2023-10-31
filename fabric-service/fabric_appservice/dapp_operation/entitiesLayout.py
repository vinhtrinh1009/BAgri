from exceptions import SchemaError
import copy


def genLayout(input):
    try:
        baseType = ["string", "int"]
        baseVar = [
            "err",
            "objId",
            "exists",
            "newObj",
            "newObjJSON",
            "result",
            "obj",
            "updateObjJSON",
            "id",
            "temp",
            "targetObj",
            "s",
            "i",
            "assetJSON",
            "objJSON",
            "new_cid",
            "priv_data",
            "response",
        ]
        allowedEncryptType = ["AES", "RSA"]

        def variableNameExists(result, variable):
            if variable in result["entities"]:
                return True
            for e in result["entities"]:
                if variable in result["entities"][e]["attributes"]:
                    return True
                if variable in result["entities"][e]["privates"]:
                    return True
                if variable in result["entities"][e]["files"]:
                    return True
            return False

        def getVarriableName(result, variable):
            name = variable
            i = 0
            while variableNameExists(result, name):
                i = i + 1
                name = f"{variable}_{i}"
            return name

        def setRelationship(result, name1, name2, type1, type2):
            if not name1 in result["relationships"]:
                result["relationships"][name1] = {}
            if not name2 in result["relationships"]:
                result["relationships"][name2] = {}
            result["relationships"][name1][name2] = {"name": name2, "type": type1}
            result["relationships"][name2][name1] = {"name": name1, "type": type2}
            return result

        result = {}
        result["entities"] = {}
        result["relationships"] = {}
        result["variables"] = {}
        result["encryptionType"] = "AES"
        
        if "encryption_type" in input and input["encryption_type"].upper() in allowedEncryptType:
            result["encryptionType"] = input["encryption_type"].upper()

        for e in input["entities"]:
            result["entities"][e["name"]] = copy.deepcopy(e)
            result["entities"][e["name"]]["attributes"] = {}
            result["entities"][e["name"]]["files"] = {}
            result["entities"][e["name"]]["privates"] = {}
            for a in e["attributes"]:
                if a["type"] in baseType:
                    if "encrypt" in a and a["encrypt"]:
                        result["entities"][e["name"]]["privates"][
                            a["name"]
                        ] = copy.deepcopy(a)
                    else:
                        result["entities"][e["name"]]["attributes"][
                            a["name"]
                        ] = copy.deepcopy(a)
                elif a["type"] == "file":
                    result["entities"][e["name"]]["files"][a["name"]] = copy.deepcopy(a)

        for e in result["entities"]:
            result["entities"][e]["attributes"][result["entities"][e]["primary_key"]][
                "type"
            ] = "string"
            if not e in result["relationships"]:
                result["relationships"][e] = {}
            if "relationships" in result["entities"][e]:
                for r in result["entities"][e]["relationships"]:
                    setRelationship(
                        result, e, r["reference_to_entity"], r["type"][-1].lower(), r["type"][0].lower()
                    )

        doc_layout = {}
        doc_layout["dapp_name"] = input["dapp_name"]
        doc_layout["dapp_description"] = input["dapp_description"]

        folder_tree = [
            {
                "name": "cli",
                "children": [
                    {"name": "enrollAmin.js", "description": "Enroll Admin file."},
                    {"name": "registerUser.js", "description": "Register User."},
                ],
            },
            {
                "name": "connection-files",
                "children": [
                    {
                        "name": "ccp.json",
                        "description": "Connection Profile json file.",
                    },
                ],
            },
            {
                "name": "encryption",
                "children": [
                    {
                        "name": "RSA.js",
                        "description": "Enrcryption Object using RSA.",
                    },
                    {
                        "name": "AES.js",
                        "description": "Enrcryption Object using AES.",
                    },
                ],
            },
            {
                "name": "fabric",
                "children": [
                    {
                        "name": "network.js",
                        "description": "Chaincode Interaction SDK file.",
                    },
                ],
            },
            {
                "name": "storage",
                "children": [
                    {
                        "name": "storage.js",
                        "description": "V-storage Interaction to upload file.",
                    },
                ],
            },
            {"name": "package.json", "description": "Package."},
        ]

        getting_started = [
            {
                "instruction": "Install requirement package",
                "description": "Open Terminal, change directory to SDK folder and run below command",
                "commands": [
                    {"language": "bash", "command": "npm install"},
                ],
            },
            {
                "instruction": "Enroll Admin",
                "commands": [
                    {
                        "language": "bash",
                        "command": "node ./cli/enrollAmin.js --org=[orgname] ",
                    },
                ],
            },
            {
                "instruction": "Register User",
                "commands": [
                    {
                        "language": "bash",
                        "command": "node ./cli/registerUser.js --org=[orgname] --username=[username] ",
                    },
                ],
            },
            {
                "instruction": "Import Encryption",
                "commands": [
                    {
                        "language": "javascript",
                        "command": "const AES = require('./encryption/AES.js');",
                    },
                ],
            },
            {
                "instruction": "Import SDK",
                "commands": [
                    {
                        "language": "javascript",
                        "command": "const network = require('./fabric/network');",
                    },
                ],
            },
            {
                "instruction": "Connect to network",
                "commands": [
                    {
                        "language": "javascript",
                        "command": "let obj = await network.connectToNetwork(organizationName, userName, secret);",
                    },
                ],
            },
            {
                "instruction": "Development with function in SDK",
            },
        ]

        functions = []

        # aes_class = {
        #     "name": "AES class",
        #     "description": "Encryption Object using AES",
        #     "parameters": [
        #         {
        #             "name": "secret",
        #             "type": "string",
        #             "description": "Secret used to encrypt and decrypt",
        #         },
        #     ],
        #     "returns": {
        #         "type": "object",
        #         "description": "New AES encryption Object",
        #     },
        # }

        # rsa_class = {
        #     "name": "RSA class",
        #     "description": "Encryption Object using RSA",
        #     "parameters": [
        #         {
        #             "name": "privateKey",
        #             "type": "string",
        #             "description": "Private Key for RSA Encryption",
        #         },
        #     ],
        #     "returns": {
        #         "type": "object",
        #         "description": "New AES encryption Object",
        #     },
        # }

        connectNetwork_function = {
            "name": "network.connectToNetwork",
            "description": "Connect to network",
            "parameters": [
                {
                    "name": "orgName",
                    "type": "string",
                    "description": "Organization name",
                },
                {"name": "username", "type": "string", "description": "Username"},
                {
                    "name": "secret",
                    "type": "string",
                    "description": 'Encrypt Secret, Private Key',
                },
            ],
            "returns": {
                "type": "object",
                "description": "Network Object",
                "fields": [
                    {
                        "name": "contract",
                        "type": "object",
                        "description": "Contract object",
                    },
                    {
                        "name": "network",
                        "type": "object",
                        "description": "Network object",
                    },
                    {
                        "name": "gateway",
                        "type": "object",
                        "description": "Gateway object",
                    },
                    {
                        "name": "username",
                        "type": "string",
                        "description": "Username",
                    },
                    {
                        "name": "readSecret",
                        "type": "string",
                        "description": "Secret use to decrypt data",
                    },
                    {
                        "name": "writeSecret",
                        "type": "string",
                        "description": "Secret use to encrypt data",
                    },
                ],
            },
        }

        functions.append(connectNetwork_function)

        for e in result["entities"]:
            f_name = "network.Create" + e
            f_parameters = []
            f_description = f"Create {e}"

            f_sub_parameters = []

            networkObj_param = {
                "name": "networkObj",
                "type": "object",
                "description": "Object created using network.connectToNetwork",
            }

            for a in result["entities"][e]["attributes"]:
                parameter = {
                    "name": a,
                    "type": result["entities"][e]["attributes"][a]["type"],
                    "description": f"{a} of {e}",
                }
                f_sub_parameters.append(parameter)
            for p in result["entities"][e]["privates"]:
                parameter = {
                    "name": p,
                    "type": result["entities"][e]["privates"][p]["type"],
                    "description": f"{p} of {e}",
                }
                f_sub_parameters.append(parameter)
            for f in result["entities"][e]["files"]:
                parameter = {
                    "name": f,
                    "type": "string",
                    "description": f"Path to {f} of {e}",
                }
                f_sub_parameters.append(parameter)

            other_param = {
                "name": f"{e}Created",
                "type": "object",
                "description": f"Created {e} object",
                "fields": f_sub_parameters,
            }

            f_parameters.append(copy.deepcopy(networkObj_param))

            f_parameters.append(other_param)

            f_returns = {
                "type": "object",
                "description": "Result Object",
                "fields": [
                    {
                        "name": "success",
                        "type": "boolean",
                        "description": "Submit transaction successfully or not",
                    },
                    {"name": "msg", "type": "string", "description": "Message"},
                    {"name": "err", "type": "object", "description": "Error"},
                ],
            }

            f = {
                "name": f_name,
                "description": f_description,
                "parameters": f_parameters,
                "returns": f_returns,
            }
            functions.append(f)

            f_name = "network.Read" + e
            f_parameters = []
            f_description = f"Read {e}"

            other_param = {
                "name": f"{e}_pk",
                "type": "string",
                "description": f"{e} primary key",
            }

            f_parameters.append(copy.deepcopy(networkObj_param))

            f_parameters.append(other_param)

            f_returns = {
                "type": "object",
                "description": "Result Object",
                "fields": [
                    {
                        "name": "success",
                        "type": "boolean",
                        "description": "Evaluate transaction successfully or not",
                    },
                    {"name": "msg", "type": "string", "description": "Message"},
                    {"name": "result", "type": "object", "description": f"{e} object"},
                    {"name": "err", "type": "object", "description": "Error"},
                ],
            }

            f = {
                "name": f_name,
                "description": f_description,
                "parameters": f_parameters,
                "returns": f_returns,
            }
            functions.append(f)

            update_function = copy.deepcopy(functions[-2])
            update_function["name"] = "network.Update" + e
            update_function["description"] = f"Update {e}"
            update_function["parameters"][1]["name"] = f"{e}Updated"
            update_function["parameters"][1]["description"] = f"Updated {e} information"

            functions.append(update_function)

            delete_function = copy.deepcopy(functions[-2])
            delete_function["name"] = "network.Delete" + e
            delete_function["description"] = f"Delete {e}"
            delete_function["returns"]["fields"][0][
                "description"
            ] = "Submit transaction successfully or not"
            delete_function["returns"]["fields"].pop(2)

            functions.append(delete_function)

            for relationship in result["relationships"][e]:
                r = result["relationships"][e][relationship]
                e_param = {
                    "name": f"{e}_pk",
                    "type": "string",
                    "description": f"{e} primary key",
                }
                r_param = {
                    "name": "{}_pk".format(r["name"]),
                    "type": "string",
                    "description": f"{e} primary key",
                }
                if r["type"] == "1":
                    f_name = "network.Set{}for{}".format(r["name"], e)
                    f_description = "Set {} for {}".format(r["name"], e)
                    f_parameters = []
                    f_parameters.append(copy.deepcopy(networkObj_param))
                    f_parameters.append(e_param)
                    f_parameters.append(r_param)
                    f_returns = copy.deepcopy(functions[-1]["returns"])
                    f = {
                        "name": f_name,
                        "description": f_description,
                        "parameters": f_parameters,
                        "returns": f_returns,
                    }
                    functions.append(f)

                    f_name = "network.Unset{}for{}".format(r["name"], e)
                    f_description = "Unset {} for {}".format(r["name"], e)
                    f_parameters = []
                    f_parameters.append(copy.deepcopy(networkObj_param))
                    f_parameters.append(e_param)
                    f_returns = copy.deepcopy(functions[-1]["returns"])
                    f = {
                        "name": f_name,
                        "description": f_description,
                        "parameters": f_parameters,
                        "returns": f_returns,
                    }
                    functions.append(f)
                elif r["type"] == "n":
                    f_name = "network.Add{}for{}".format(r["name"], e)
                    f_description = "Add {} for {}".format(r["name"], e)
                    f_parameters = []
                    f_parameters.append(copy.deepcopy(networkObj_param))
                    f_parameters.append(e_param)
                    f_parameters.append(r_param)
                    f_returns = copy.deepcopy(functions[-1]["returns"])
                    f = {
                        "name": f_name,
                        "description": f_description,
                        "parameters": f_parameters,
                        "returns": f_returns,
                    }
                    functions.append(f)

                    f_name = "network.Remove{}for{}".format(r["name"], e)
                    f_description = "Remove {} for {}".format(r["name"], e)
                    f_parameters = []
                    f_parameters.append(copy.deepcopy(networkObj_param))
                    f_parameters.append(e_param)
                    f_parameters.append(r_param)
                    f_returns = copy.deepcopy(functions[-1]["returns"])
                    f = {
                        "name": f_name,
                        "description": f_description,
                        "parameters": f_parameters,
                        "returns": f_returns,
                    }
                    functions.append(f)

        doc_layout["folder_tree"] = folder_tree
        doc_layout["getting_started"] = getting_started
        doc_layout["functions"] = functions

        result["doc_layout"] = doc_layout

        for v in baseVar:
            name = getVarriableName(result, v)
            result["variables"][v] = name

        return result

    except Exception as e:
        raise SchemaError(e)
