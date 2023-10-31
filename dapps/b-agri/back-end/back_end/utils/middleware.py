from aiohttp.web import middleware
import jwt
from utils.response import ApiNotFound, ApiUnauthorized

NO_AUTH_ROUTES = [
    '/v1/login',
    '/v1/registry',
    '/v1/seasons/network',
    '/v1/reset-password',
]

@middleware
async def self_authorize(request, handler):
    if request.method != "OPTIONS":
        if request.path in NO_AUTH_ROUTES or request.path.startswith("/static/qr_codes"):
            resp = await handler(request)
            return resp
        else:
            token = request.headers.get("AUTHORIZATION")
            if token is None:
                raise ApiUnauthorized("No auth token provided!")

            token_prefixes = ("Bearer", "Token")
            for prefix in token_prefixes:
                if prefix in token:
                    token = token.partition(prefix)[2].strip()
            try:
                user_info = jwt.decode(
                    token,
                    request.app["config"]["jwt_key"],
                    algorithms=['HS256'])
            except BaseException:
                raise ApiUnauthorized('Invalid auth token')

            # FIXME: I cannot find other way to check if the handler is 404 :D
            if "404" in str(handler):
                return ApiNotFound("Route not found")

            if request.path.startswith("/static"):
                return await handler(request)
            resp = await handler(request, user_info)
            return resp
    else:
        resp = await handler(request)
        return resp
