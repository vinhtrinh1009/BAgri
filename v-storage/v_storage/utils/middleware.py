from aiohttp.web import middleware
import jwt
from utils.response import ApiUnauthorized
from utils.handle_account import *
from utils.logging import get_logger

_LOGGER = get_logger(__name__)

@middleware
async def authorized(request, handler):
    if request.method != "OPTIONS":
        parent_id = request.match_info.get("folder_id", "")
        sdk_key = None
        if "sdk_key" in request.rel_url.query:
            sdk_key = request.rel_url.query["sdk_key"]
        token = request.headers.get("AUTHORIZATION")
        if sdk_key is None:
            if token is None:
                raise ApiUnauthorized("No auth token provided!")
            else:
                token_prefixes = ("Bearer", "Token")
                for prefix in token_prefixes:
                    if prefix in token:
                        token = token.partition(prefix)[2].strip()
                try:
                    user_info = jwt.decode(token, request.app["config"]["jwt_key"], algorithms=['HS256'])
                except:
                    raise ApiUnauthorized('Invalid auth token')
                resp = await handler(request, user_info)
                return resp
        else:
            token = get_token()["data"]["token"]
            dapps = get_info_by_sdk_key(token, sdk_key)["data"]
            if len(dapps) == 0:
                raise ApiUnauthorized('Invalid sdk key')
            elif len(dapps) > 1:
                raise ApiUnauthorized(f'More than one dapp have sdk_key is {sdk_key}')
            dapp = dapps[0]
            data_folder_id = dapp["data_folder_id"]
            if parent_id != data_folder_id:
                raise ApiUnauthorized(f'Invalid sdk key 2 {parent_id} / {data_folder_id}')
            user_info = jwt.decode(token, request.app["config"]["jwt_key"], algorithms=['HS256'])
            resp = await handler(request, user_info)
            return resp
    else:
        resp = await handler(request)
        return resp