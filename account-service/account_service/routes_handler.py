import json
import re
import asyncio
from constants import regex, message, role
from user.routes_handler import UserHandler
from utils.logging import get_logger
from utils.response import *
from json import JSONDecodeError

_LOGGER = get_logger(__name__)

class RouteHandler:
    def __init__(self, database):
        self._user_handler = UserHandler(database)
    
    async def login(self, request):
        _LOGGER.info("Logging")
        body = await decode_request(request)
        required_fields = ["username", "password"]
        validate_fields(required_fields, body)
        response = await self._user_handler.login(body)
        return response

    async def create_user(self, request):
        _LOGGER.info("Create new user")
        body = await decode_request(request)
        required_fields = ["username", "password", "full_name", "email", "phone"]
        validate_fields(required_fields, body)
        response = await self._user_handler.create_user(body)
        return response
    
    async def get_user_info(self, request,user_info):
        _LOGGER.info("Get user info")
        user_id=user_info["user_id"]
        response = await self._user_handler.get_user_info(user_id)
        return response

    async def update_user(self, request, user_info):
        user_id = request.match_info.get("user_id", "")
        if user_info["role"] != role.ADMIN:
            if user_info["user_id"] != user_id:
                return ApiUnauthorized(message.FORBIDDEN)
        _LOGGER.info(f"Update user {user_info['user_id']}")
        body = await decode_request(request)
        required_fields = body.keys()
        validate_fields(required_fields, body)
        response = await self._user_handler.update_user(body, user_id)
        return response

    async def verify_email(self, request,user_info):
        user_id = request.match_info.get("user_id", "")    
        if user_info["role"] != role.ADMIN:
            if user_info["user_id"] != user_id:
                return ApiUnauthorized(message.FORBIDDEN)   
        _LOGGER.info(f"Verify email {user_id}")
        body = await decode_request(request)
        required_fields = body.keys()
        validate_fields(required_fields, body)
        response = await self._user_handler.verify_email(body,user_id)
        return response
    
    async def verify_password(self, request,user_info):
        user_id = request.match_info.get("user_id", "")    
        if user_info["role"] != role.ADMIN:
            if user_info["user_id"] != user_id:
                return ApiUnauthorized(message.FORBIDDEN)   
        _LOGGER.info(f"Verify password {user_id}")
        body = await decode_request(request)
        required_fields = body.keys()
        validate_fields(required_fields, body)
        response = await self._user_handler.verify_password(body,user_id)
        return response

    async def disable_user(self, request, user_info):
        user_id = request.match_info.get("user_id", "")
        if user_info["role"] != role.ADMIN:
            if user_info["user_id"] != user_id:
                return ApiUnauthorized(message.FORBIDDEN)
        _LOGGER.info(f"Disable user {user_info['user_id']}")
        response = await self._user_handler.disable_user(user_id)
        return response

    async def enable_user(self, request, user_info):
        user_id = request.match_info.get("user_id", "")
        if user_info["role"] != role.ADMIN:
            if user_info["user_id"] != user_id:
                return ApiUnauthorized(message.FORBIDDEN)
        _LOGGER.info(f"Enable user {user_info['user_id']}")
        response = await self._user_handler.enable_user(user_id)
        return response

    async def send_email_verify(self, request, user_info):
        user_id = request.match_info.get("user_id", "")
        if user_info["role"] != role.ADMIN:
            if user_info["user_id"] != user_id:
                return ApiUnauthorized(message.FORBIDDEN)
        _LOGGER.info(f"send_email_verify_pwd {user_info['user_id']}")
        response = await self._user_handler.send_email_verify(user_id)
        return response

    async def change_password(self, request, user_info):
        user_id = request.match_info.get("user_id", "")
        if user_info["role"] != role.ADMIN:
            if user_info["user_id"] != user_id:
                return ApiUnauthorized(message.FORBIDDEN)
        _LOGGER.info(f"Change password {user_info['user_id']}")
        body = await decode_request(request)
        required_fields = body.keys()
        validate_fields(required_fields, body)
        response = await self._user_handler.change_password(body, user_id)
        return response
    
    
async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest('Improper JSON format')



def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise ApiBadRequest(
                f"{field} parameter is required")
        elif field == 'username':
            if not re.match(regex.USERNAME_REGEX, body["username"]):
                raise ApiBadRequest(message.INVALID_USERNAME)
        elif field == 'password':
            if not re.match(regex.PASSWORD_REGEX, body["password"]):
                raise ApiBadRequest(message.INVALID_PASSWORD)
        elif field == 'email':           
            if not re.match(regex.EMAIL_REGEX, body["email"]) :
                raise ApiBadRequest(message.INVALID_EMAIL)
        elif field == 'full_name':
            if not re.match(regex.NAME_REGEX, body["full_name"]) :
                raise ApiBadRequest(message.INVALID_NAME)
        elif field == 'location':
            if not re.match(regex.LOCATION_REGEX, body["location"]):
                raise ApiBadRequest(message.INVALID_LOCATION)
        elif field == 'phone':
            if not re.match(regex.PHONE_REGEX, body["phone"]):
                raise ApiBadRequest(message.INVALID_PHONE)
        elif field == 'birthday':
            if not re.match(regex.DATE_REGEX, body["birthday"]):
                raise ApiBadRequest(message.INVALID_DATE)
        