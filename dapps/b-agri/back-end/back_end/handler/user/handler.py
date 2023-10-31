import bcrypt
import jwt
from pymongo.errors import DuplicateKeyError
from settings import config
from utils.logging import get_logger
from utils.response import ApiBadRequest, success

_LOGGER = get_logger(__name__)


class UserHandler:
    def __init__(self, database):
        self.__database = database

    async def login(self, body):
        err_msg = "Tên đăng nhập hoặc mật khẩu không đúng"
        user = await self.__database.conn.user.find_one({'username': body['username']})
        if not user:
            return ApiBadRequest(err_msg)

        if bcrypt.checkpw(
                body['password'].encode('utf-8'),
                user['password'].encode('utf-8')):
            user = {
                "id": str(user['_id']),
                "username": user['username'],
                "fullname": user['fullname'],
                "role": user['role']
            }
            jwt_token = jwt.encode(
                user,
                config['jwt_key'],
                algorithm='HS256')
            return success({
                "user_id": user['id'],
                "token": jwt_token
            })
        else:
            return ApiBadRequest(err_msg)

    async def get_users(self):
        return success({
            "users": [{
                "user_id": "61971de8d305bde3e0598b79",
                "username": "usertest",
                "fullname": "Nguyen Van An",
                "password": "87acec17cd9dcd20a716cc2cf67417b71c8a7016",
                "role": "ktv"
            },
                {
                "user_id": "61971de8d305bde3e0598b80",
                "username": "usertest",
                "fullname": "Tran Van B",
                "password": "87acec17cd9dcd20a716cc2cf67417b71c8a7016",
                "role": "qlv"
            }]
        })

    async def get_user(self, user_id):
        return success({
            "user": {
                "user_id": user_id,
                "username": "usertest",
                "fullname": "Nguyen Van An",
                "password": "87acec17cd9dcd20a716cc2cf67417b71c8a7016",
                "role": "ktv"
            }
        })

    async def create_user(self, new_user):
        hash_password = bcrypt.hashpw(
            new_user['password'].encode('utf-8'),
            bcrypt.gensalt())
        new_user['password'] = hash_password.decode('utf-8')

        try:
            user = await self.__database.conn.user.insert_one(new_user)
            new_user['user_id'] = str(user.inserted_id)
            new_user.pop('password')
            new_user.pop('_id')
            return success({
                "user": new_user
            })
        except DuplicateKeyError:
            return ApiBadRequest("username is existed")

    async def reset_password(self, body):
        """reset user password back to user phone"""
        user = await self.__database.conn.user.find_one(
                {"username": body["username"], "phone": body["phone"]})

        if not user:
            return ApiBadRequest("Số điện thoại hoặc tên đăng nhập không đúng")

        hash_reset_password = bcrypt.hashpw(
            body['phone'].encode('utf-8'),
            bcrypt.gensalt())

        modification = {
            "password": hash_reset_password.decode('utf-8')
        }

        await self.__database.conn.user.find_one_and_update(
            {"username": body["username"], "phone": body["phone"]},
            {"$set": modification}
        )

        return success({
            "id": str(user["_id"]),
            "username": body["username"],
            "phone": body["phone"]
        })

    async def change_password(self, body, user_info):
        user = await self.__database.conn.user.find_one({'username': user_info['username']})
        if not user:
            return ApiBadRequest("Tên đăng nhập không tồn tại")

        if bcrypt.checkpw(
                body['old_password'].encode('utf-8'),
                user['password'].encode('utf-8')):
            if body["new_password"] == body["retype_new_password"]:
                hash_new_password = bcrypt.hashpw(
                    body['new_password'].encode('utf-8'),
                    bcrypt.gensalt())
                modification = {
                    "password": hash_new_password.decode('utf-8')
                }

                await self.__database.conn.user.find_one_and_update(
                    {'username': user_info['username']},
                    {'$set': modification}
                )

                return success({
                    "id": user_info["id"],
                    "username": user_info["username"]
                })
            else:
                return ApiBadRequest("Mật khẩu nhập lại khác mật khẩu ban đầu")
        else:
            return ApiBadRequest("Mật khẩu không đúng")

    async def update_user(self, user_id, update_user):
        return success({
            "updated_user": {
                "user_id": user_id,
                "username": "usertest",
                "fullname": "Nguyen Van An",
                "password": "87acec17cd9dcd20a716cc2cf67417b71c8a7016",
                "role": "qlv"
            }
        })

    async def get_mangers(self):
        managers = await self.__database.conn.user.find(
            {"role": "qlv"},
            {"password": 0, "username": 0}).to_list(length=None)
        for manager in managers:
            manager["manager_id"] = str(manager["_id"])
            manager.pop("_id")

        return success({
            "managers": managers
        })

    async def delete_user(self, user_id):
        return success({
            "user_id": user_id
        })
