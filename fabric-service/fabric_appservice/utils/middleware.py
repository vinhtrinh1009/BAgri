from aiohttp.web import middleware
import jwt

from utils.response import ApiUnauthorized


@middleware
async def self_authorize(request, handler):
    token = request.headers.get("AUTHORIZATION")
    if token is None:
        raise ApiUnauthorized("No auth token provided!")

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
