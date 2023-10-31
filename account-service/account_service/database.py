import asyncio
import motor.motor_asyncio as aiomotor
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError

from utils.logging import get_logger

_LOGGER = get_logger(__name__)

class Database:
    def __init__(self, host, port, username, password, dbname):
        self._mongo_uri = f"mongodb://{username}:{password}@{host}:{port}"
        self._dbname = dbname
        self._conn = None
    
    async def connect(self, retries=2, delay=1):
        _LOGGER.info(f"Connecting to database on {self._mongo_uri}")

        for attemt in range(retries):
            try:
                self._conn = aiomotor.AsyncIOMotorClient(self._mongo_uri)[self._dbname]
                _LOGGER.info(f"List collection: {await self._conn.list_collection_names()}")
                _LOGGER.info("Successfully connected to the database")
                return
            except ServerSelectionTimeoutError:
                if attemt == retries-1:
                    _LOGGER.error("Cannot connect to the database")
                    raise ServerSelectionTimeoutError
                else:
                    _LOGGER.debug("Database connection failed")
                    await asyncio.sleep(delay)
        
    async def get_user(self, **kwargs):
        if "_id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs["_id"])
        users = self._conn["users"].find(kwargs)
        async for user in users:
            user["user_id"] = str(user["_id"])
            user.pop("_id", None)
            return user

    async def create_user(self, new_user):
        result = await self._conn["users"].insert_one(new_user)
        user_id = str(result.inserted_id)
        return user_id
        
    async def update_user(self, user_id, modification):
        user_filter = {
            "_id": ObjectId(user_id)
        }
        updated_user = await self._conn["users"].find_one_and_update(
                                                    {"_id": ObjectId(user_id)},
                                                    {'$set': modification},
                                                    return_document=ReturnDocument.AFTER)
        
        updated_user["user_id"] = str(updated_user["_id"])
        updated_user.pop("_id", None)
        return updated_user

    async def delete_user(self, user_id):
        user_filter = {
            "_id": ObjectId(user_id)
        }
        result = await self._conn["users"].delete_many(user_filter)
        return {
            "number_deleted_users": result.deleted_count
        }