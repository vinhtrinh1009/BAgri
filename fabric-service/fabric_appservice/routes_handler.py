# from utils.request import decode_request
# from utils.response import success
# from utils.logging import get_logger
# from network.handler import NetworkHandler
# from dapp.handler import DappHandler
# from aiohttp import web

# _LOGGER = get_logger(__name__)


# class RouteHandler(object):
#     def __init__(self, database, broker_client):
#         self._network_handler = NetworkHandler(database, broker_client)
#         self._dapp_handler = DappHandler(database, broker_client)

#     async def create_network(self, request, user_info):
#         _LOGGER.debug("Create a new network")
#         body = await decode_request(request)
#         response = await self._network_handler.create_network(user_info=user_info, new_network=body)
#         return response
#         # write database
#         # generate_network.gen_code(data=network_config)
#         # generate_network.deploy_network(data=network_config)

#     async def create_dapp(self, request, user_info):
#         _LOGGER.debug("Create a dapp network")
#         body = await decode_request(request)
#         response = await self._dapp_handler.create_dapp(user_info=user_info, new_dapp=body)
#         return response

#     async def download_sdk(self, request, user_info):
#         _LOGGER.debug("Download sdk")
#         dapp_name = request.match_info.get("name", "")
#         response = web.FileResponse('test.zip')
#         return response



#     # async def create_dapp(self, request):
#     #     body = await decode_request(request)
#     #     # // get database domain from network id     goi la network_name
#     #     network_name = "test-thu"
#     #
#     #     chaincode_config = {
#     #         "domain": network_name,
#     #         "objects": []
#     #     }
#     #     # get orgs = []
#     #     orgs = ["BK", "DHCONGNGHE"]
#     #     for entity in body["entities"]:
#     #         properties = []
#     #         fields = []
#     #         for att in entity["attributes"]:
#     #             if att["name"] != entity["primary_key"]:
#     #                 properties.append(att)
#     #                 fields.append({
#     #                     "name": att["name"],
#     #                     "type": att["type"],
#     #                     "typeRelationship": "none"
#     #                 })
#     #             else:
#     #                 fields.append({
#     #                     "name": att["name"],
#     #                     "type": att["type"],
#     #                     "typeRelationship": ""
#     #                 })
#     #
#     #         object = {
#     #             "name": entity["name"],
#     #             "name_many": entity["name"] + "s",
#     #             "create": {
#     #                 "msp": orgs,
#     #                 "function_name": "Create"+ entity["name"]
#     #             },
#     #             "update":{
#     #                 "msp": orgs,
#     #                 "function_name": "Update"+entity["name"]
#     #             },
#     #             "delete": None,
#     #             "properties": properties,
#     #             "fields": fields,
#     #             "inclusion": [],
#     #             "is_inclused": [],
#     #             "dependence": [],
#     #             "is_dependenced": [],
#     #             "owner": [],
#     #             "is_owned": [],
#     #             "match": [],
#     #             "is_matched": [],
#     #             "relationship": "",
#     #             "relatedObj": [],
#     #             "newField": ""
#     #         }
#     #         chaincode_config["objects"].append(object)
#     #
#     #     generate_dapp.gen_code(data=chaincode_config, username="quandinh", domain="test-fabric")
#     #     return success(chaincode_config)

