from json.decoder import JSONDecodeError

from utils.logging import get_logger
from network.routes_handler import NetworkHandler
from dapp.routes_handler import DappHandler
from utils.response import success, ApiBadRequest

from aiohttp.web import json_response

_LOGGER = get_logger(__name__)


class RouteHandler:
    def __init__(self, database, broker_client):
        self._network_handler = NetworkHandler(database, broker_client)
        self._dapp_handler = DappHandler(database, broker_client)

    async def create_network(self, request, user_info):
        _LOGGER.debug("Create a new network")
        body = await decode_request(request)
        # _LOGGER.debug(body)
        required_fields = ["name", "blockchain_type", "consensus",
                           "node_infrastructure", "blockchain_peer_config"]
        validate_fields(required_fields, body)

        response = await self._network_handler.create_network(user_info=user_info, new_network=body)
        return response

    async def retry_create_network(self, request, user_info):
        network_id = request.match_info.get("network_id", "")
        _LOGGER.debug(f"Retry create network: {network_id}")
        response = await self._network_handler.retry_create_network(user_info=user_info, network_id=network_id)
        return response

    async def update_network(self, request, user_info):
        network_id = request.match_info.get("network_id", "")
        _LOGGER.debug(f"Update a network: {network_id}")
        body = await decode_request(request)
        # _LOGGER.debug(body)
        required_fields = ["update_type", "config"]
        validate_fields(required_fields, body)

        response = await self._network_handler.update_network(user_info=user_info, network_id=network_id, update_info=body)
        return response

    async def retry_update_network(self, request, user_info):
        network_id = request.match_info.get("network_id", "")
        _LOGGER.debug(f"Retry update a network: {network_id}")
        response = await self._network_handler.retry_update_network(user_info=user_info, network_id=network_id)
        return response

    async def rollback_update_network(self, request, user_info):
        network_id = request.match_info.get("network_id", "")
        _LOGGER.debug(f"Rollback update a network: {network_id}")
        response = await self._network_handler.rollback_update_network(user_info=user_info, network_id=network_id)
        return response

    async def get_user_networks(self, request, user_info):
        _LOGGER.debug(f"Get all networks of the user: {user_info['user_id']}")
        response = await self._network_handler.get_user_networks(user_info)
        return response

    async def get_network(self, request, user_info):
        network_id = request.match_info.get("network_id", "")
        _LOGGER.debug(f"Get a network: {network_id}")
        user_id = user_info["user_id"]
        response = await self._network_handler.get_network(user_id=user_id, network_id=network_id)
        return response

    async def delete_network(self, request, user_info):
        network_id = request.match_info.get("network_id", "")
        _LOGGER.debug(f"Delete a network: {network_id}")
        response = await self._network_handler.delete_network(user_info=user_info, network_id=network_id)
        return response

    async def create_resource(self, request, user_info):
        body = await decode_request(request)
        network_id = request.match_info.get("network_id", "")
        _LOGGER.debug(f"Create new resource of network: {network_id}")
        required_fields = ["resource_name", "resource_config", "resource_description"]
        validate_fields(required_fields, body)
        response = await self._network_handler.create_resource(user_info=user_info, network_id=network_id, new_resource=body)
        return response
    
    async def get_network_resources(self, request, user_info):
        user_id = user_info["user_id"]
        network_id = request.match_info.get("network_id", "")
        _LOGGER.debug(f"Get all resources of the network: {network_id}")
        response = await self._network_handler.get_network_resources(network_id)
        return response

    async def create_dapp(self, request, user_info):
        body = await decode_request(request)
        _LOGGER.debug(f"Create a new dapp {body}")
        required_fields = ["entities", "network_id"]
        validate_fields(required_fields, body)

        response = await self._dapp_handler.create_dapp(user_info=user_info, new_dapp=body)
        return response

    async def retry_create_dapp(self, request, user_info):
        dapp_id = request.match_info.get("dapp_id", "")
        _LOGGER.debug(f"Retry create dapp: {dapp_id}")
        response = await self._dapp_handler.retry_create_dapp(dapp_id=dapp_id, user_info=user_info)
        return response

    async def update_dapp(self, request, user_info):
        dapp_id = request.match_info.get("dapp_id", "")
        _LOGGER.debug(f"Update dapp: {dapp_id}")
        body = await decode_request(request)
        required_fields = ["entities", "network_id"]
        validate_fields(required_fields, body)

        response = await self._dapp_handler.update_dapp(dapp_id=dapp_id, user_info=user_info, update_dapp=body)
        return response

    async def retry_update_dapp(self, request, user_info):
        dapp_id = request.match_info.get("dapp_id", "")
        _LOGGER.debug(f"Retry update dapp: {dapp_id}")
        response = await self._dapp_handler.retry_update_dapp(dapp_id=dapp_id, user_info=user_info)
        return response

    async def rollback_update_dapp(self, request, user_info):
        dapp_id = request.match_info.get("dapp_id", "")
        _LOGGER.debug(f"Rollback update dapp: {dapp_id}")
        response = await self._dapp_handler.rollback_update_dapp(dapp_id=dapp_id, user_info=user_info)
        return response

    async def get_user_dapps(self, request, user_info):
        user_id = user_info["user_id"]
        _LOGGER.debug(f"Get all dapps of the user: {user_id}")
        response = await self._dapp_handler.get_user_dapps(user_id)
        return response

    async def get_dapp(self, request, user_info):
        dapp_id = request.match_info.get("dapp_id", "")
        _LOGGER.debug(f"Get a dapp: {dapp_id}")
        user_id = user_info["user_id"]
        response = await self._dapp_handler.get_dapp(user_id=user_id, dapp_id=dapp_id)
        return response

    async def delete_dapp(self, request, user_info):
        dapp_id = request.match_info.get("dapp_id", "")
        _LOGGER.debug(f"Delete a dapp: {dapp_id}")
        response = await self._dapp_handler.delete_dapp(user_info=user_info, dapp_id=dapp_id)
        return response

    async def retry_delete_dapp(self, request, user_info):
        dapp_id = request.match_info.get("dapp_id", "")
        _LOGGER.debug(f"Retry delete a dapp: {dapp_id}")
        response = await self._dapp_handler.retry_delete_dapp(user_info=user_info, dapp_id=dapp_id)
        return response

    async def get_dapp_by_sdk_key(self, request, user_info):
        sdk_key = request.match_info.get("sdk_key", "")
        _LOGGER.debug(f"Get dapp by sdk_key: {sdk_key}")
        response = await self._dapp_handler.get_dapp_by_sdk_key(sdk_key=sdk_key)
        return response

    async def healthz(self, request, user_info):
        return json_response({"status": "success"}, status=200)


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest('Improper JSON format')


def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise ApiBadRequest(
                "'{}' parameter is required".format(field))
