import asyncio
from utils.mail import  otp_code, send_email
from utils.response import success, ApiBadRequest, ApiInternalError
from utils.logging import get_logger
from aiohttp import web
import datetime
import os
from constants import plan, role, message
from utils import security
import pyshorteners


_LOGGER = get_logger(__name__)

class UserHandler:
    def __init__(self, database):
        self.__database = database
   
    async def login(self, body):
        username = body["username"]
        password = body["password"]
        password = security.sha(password)

        user = await self.__database.get_user(username=username, password=password)
        if not user:
            return ApiBadRequest(message.WRONG_USERNAME_PASS)
        if not user["active"]:
            return ApiBadRequest(message.INACTIVE)
        
        payload = {
            "user_id": user["user_id"],
            "username": user["username"],
            "full_name":user["full_name"],
            # "avatar":avatar or user["avatar"],
            "role":user["role"]
        }
        token = security.encode_jwt(payload).decode('utf-8')
        return success({
            "message": message.LOGIN_SUCCESS,
            "token": token,
            "user_id": payload["user_id"],
            "user":user
        })

    async def create_user(self, new_user):
        user = await self.__database.get_user(username=new_user["username"])
        if user:
            return ApiBadRequest(message.EXISTING_USERNAME)
        user = await self.__database.get_user(email=new_user["email"])
        if user:
            return ApiBadRequest(message.EXISTING_EMAIL)
        user_id = await self.__database.create_user({
            "username": new_user["username"],
            "password": security.sha(new_user["password"]),
            "email": "",
            "full_name": new_user["full_name"],
            "role": role.USER,
            "location": "",
            "phone": new_user["phone"],
            "birthday": "",
            "avatar": "",
            "plan": plan.FREE,
            "created_date": str(datetime.datetime.now()),
            "active": True,
            "notification":{
                'network':{
                    "ui":False,
                    "email":False
                },
                 'dapp':{
                    "ui":False,
                    "email":False
                },
                 'token':{
                    "ui":False,
                    "email":False
                }
            },
            "temp_password":"",
            "temp_email":new_user["email"]
        })

        return success({
            "message": message.ADD_USER,
            "user_id": user_id
        })

    async def update_user(self, body, user_id):
        user = await self.__database.get_user(_id=user_id)
        if not user:
            return ApiBadRequest(message.USER_NOT_FOUND)
        modification = {}
        modification["otp"]=None
        modification["updated_date"]=str(datetime.datetime.now())
        if "password" in body:
            modification["temp_password"] = security.sha(body["password"])
        if "email" in body:
            user = await self.__database.get_user(email=body["email"])
            if user:
                return ApiBadRequest(message.EXISTING_EMAIL)
            modification["temp_email"] = body["email"]
        if "full_name" in body:
            if body["full_name"] =="":
                modification["full_name"] =user["full_name"]
            else: 
                modification["full_name"] = body["full_name"]
        
        if "role" in body:
            modification["role"] = body["role"]
        if "active" in body:
            modification["active"] = body["active"]
        if "location" in body:
            if body["location"] =="":
                modification["location"] =user["location"]
            else: 
                modification["location"] = body["location"]
        if "phone" in body:
            if body["phone"] !="":
                modification["phone"] = body["phone"]
        if "birthday" in body:
            if body["birthday"] =="":
                modification["birthday"] =user["birthday"]
            else: 
                modification["birthday"] = body["birthday"]
        if "avatar" in body:
            modification["avatar"] = body["avatar"]
        if "plan" in body:
            modification["plan"] = body["plan"]
        if "notification" in body:
            modification["notification"] = body["notification"]
        else:
            pass

        updated_user = await self.__database.update_user(user_id, modification)
        
        send_email(updated_user['email'],"personal infomation",updated_user,"")
        return success({
            "updated_user": updated_user
        })


    async def send_email_verify(self,user_id):
        otp=otp_code()
        user = await self.__database.get_user(_id=user_id)
        receiver=user["email"]
        if user["email"]=="":
            receiver=user["temp_email"]
        modification={}
        if not user:
            return ApiBadRequest(message.USER_NOT_FOUND)
        modification["otp"]=otp
        updated_user = await self.__database.update_user(user_id, modification)
        send_email(receiver,"password",updated_user,otp)
        return success({
            "updated_user": updated_user
        }) 

    async def verify_email(self,body,user_id):
        otp = body["otp"]
        email = body["email"]
        user = await self.__database.get_user(_id=user_id)
        modification={}
        if not user:
            return ApiBadRequest(message.WRONG_USERNAME_PASS)
        if not user["active"]:
            return ApiBadRequest(message.INACTIVE)
        if user["otp"]!=otp:
            return ApiBadRequest('Incorrect otp')
        modification["email"]=email
        modification["temp_email"]=None
        modification["otp"]=None
        updated_user = await self.__database.update_user(user_id, modification)
        return success({
            "updated_user": updated_user
        }) 

    async def verify_password(self,body,user_id):
        otp = body["otp"]
        password = security.sha(body["password"])
        user = await self.__database.get_user( _id=user_id)
        if not user:
            return ApiBadRequest(message.WRONG_USERNAME_PASS)
        if not user["active"]:
            return ApiBadRequest(message.INACTIVE)
        if user["otp"]!=otp:
            return ApiBadRequest('Incorrect otp')
        modification={}
        modification["password"]=password
        modification["otp"]=None
        updated_user = await self.__database.update_user(user_id, modification)
        return success({
            "message": "Change password successful",
            "user": updated_user
        }) 
    
    async def get_user_info(self,user_id):
        user = await self.__database.get_user( _id=user_id)
        if not user:
            return ApiBadRequest(message.WRONG_USERNAME_PASS)
        if not user["active"]:
            return ApiBadRequest(message.INACTIVE)
       
        return success({
            "message": "Get User Info successful",
            "user": user
        }) 

    async def disable_user(self, user_id):
        user = await self.__database.get_user(_id=user_id)
        if not user:
            return ApiBadRequest(message.USER_NOT_FOUND)
        modification = {
            "active": False
        }

        updated_user = await self.__database.update_user(user_id, modification)

        return success({
            "updated_user": updated_user
        })

    async def enable_user(self, user_id):
        user = await self.__database.get_user(_id=user_id)
        if not user:
            return ApiBadRequest(message.USER_NOT_FOUND)
        modification = {
            "active": True
        }

        updated_user = await self.__database.update_user(user_id, modification)

        return success({
            "updated_user": updated_user
        })

    

    async def change_password(self, body,user_id):
        old_password = body["old_password"]
        new_password = body["new_password"]
        old_password = security.sha(old_password)
        new_password = security.sha(new_password)
        user = await self.__database.get_user( _id=user_id)
        if not user:
            return ApiBadRequest(message.WRONG_USERNAME_PASS)
        if not user["active"]:
            return ApiBadRequest(message.INACTIVE)
        if user["password"]!=old_password:
            return ApiBadRequest('Incorrect password')
        modification={}
        modification["password"]=new_password
        updated_user = await self.__database.update_user(user_id, modification)
        send_email(updated_user['email'],"password",updated_user,"")
        return success({
            "message": "Change password successful",
            "user": updated_user
        })

    

