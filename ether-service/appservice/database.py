import asyncio
import motor.motor_asyncio as aiomotor
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError

from config.logging_config import get_logger

_LOGGER = get_logger(__name__)


class Database:
    def __init__(self, host, port, username, password, dbname):
        self._mongo_uri = "mongodb://{}:{}@{}:{}".format(username, password, host, port)
        self._dbname = dbname
        self._conn = None

    async def connect(self, retries=2, delay=1):
        _LOGGER.info("Connecting to database")

        for attempt in range(retries):
            try:
                self._conn = aiomotor.AsyncIOMotorClient(self._mongo_uri)[self._dbname]
                list_db = await self._conn.list_collection_names()
                _LOGGER.info(f"List collection: {list_db}")
                _LOGGER.info("Successfully connected to the database")
                return
            except ServerSelectionTimeoutError:
                if attempt == retries-1:
                    _LOGGER.error("Cannot connect to the database")
                    raise ServerSelectionTimeoutError
                else:
                    _LOGGER.debug("Database connection failed")
                    await asyncio.sleep(delay)

    async def create_dapp(self, new_dapp):
        result = await self._conn["dapp"].insert_one(new_dapp)
        dapp_id = str(result.inserted_id)
        return dapp_id

    async def get_dapps(self, **kwargs):
        if "dapp_id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs["dapp_id"])
            del kwargs["dapp_id"]
        _LOGGER.debug(f"LIST KWARGS: {kwargs}")
        cursor = self._conn["dapp"].find(kwargs)
        dapps = []
        async for dapp in cursor:
            dapp["dapp_id"] = str(dapp["_id"])
            dapp.pop("_id", None)
            dapps.append(dapp)
        _LOGGER.debug(f"LIST DAPP: {dapps}")
        return dapps

    async def update_dapp(self, user_id, dapp_id, modification):
        dapp_filter = {
            "_id": ObjectId(dapp_id),
            "user_id": user_id
        }
        updated_dapp = await self._conn["dapp"].find_one_and_update(dapp_filter,
                                                                    {'$set': modification},
                                                                    return_document=ReturnDocument.AFTER)
        updated_dapp["dapp_id"] = str(updated_dapp["_id"])
        updated_dapp.pop("_id", None)
        return updated_dapp

    async def delete_dapp(self, dapp_id, user_id):
        dapp_filter = {
            "_id": ObjectId(dapp_id),
            "user_id": user_id
        }
        result = await self._conn["dapp"].delete_many(dapp_filter)
        return {
            "number_deleted_dapp": result.deleted_count
        }
