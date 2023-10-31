import asyncio
import resource
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

    async def create_network(self, new_network):
        result = await self._conn["network"].insert_one(new_network)
        network_id = str(result.inserted_id)
        return network_id

    async def get_networks(self, **kwargs):
        if "network_id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs["network_id"])
            del kwargs["network_id"]
        print("kwargs: {}".format(kwargs))
        cursor = self._conn["network"].find(kwargs)
        networks = []
        async for network in cursor:
            network["network_id"] = str(network["_id"])
            network.pop("_id", None)
            networks.append(network)
        return networks

    async def update_network(self, network_id, modification):
        network_filter = {
            "_id": ObjectId(network_id)
        }
        updated_network = await self._conn["network"].find_one_and_update(network_filter,
                                                                          {'$set': modification},
                                                                          return_document=ReturnDocument.AFTER)
        updated_network["network_id"] = str(updated_network["_id"])
        updated_network.pop("_id", None)

        return updated_network

    async def delete_network(self, network_id):
        network_filter = {
            "_id": ObjectId(network_id)
        }
        result = await self._conn["network"].delete_many(network_filter)
        return {
            "number_deleted_network": result.deleted_count
        }

    async def create_resource(self, new_resource):
        result = await self._conn["resource"].insert_one(new_resource)
        resource_id = str(result.inserted_id)
        return resource_id
    
    async def get_resources(self, **kwargs):
        if "resource_id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs["resource_id"])
            del kwargs["resource_id"]
        _LOGGER.debug(f"LIST KWARGS: {kwargs}")
        cursor = self._conn["resource"].find(kwargs)
        resources = []
        async for resource in cursor:
            resource["dapp_id"] = str(resource["_id"])
            resource.pop("_id", None)
            resources.append(resource)
        _LOGGER.debug(f"LIST DAPP: {resources}")
        return resources

    async def delete_resource(self, resource_id, user_id):
        resource_filter = {
            "_id": ObjectId(resource_id),
            "user_id": user_id
        }
        result = await self._conn["resource"].delete_many(resource_filter)
        return {
            "number_deleted_dapp": result.deleted_count
        }

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

    async def create_user(self, new_user):
        result = await self._conn["user"].insert_one(new_user)
        user_id = str(result.inserted_id)
        return user_id

    async def get_users(self, **kwargs):
        if "user_id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs["user_id"])
            del kwargs["user_id"]
        _LOGGER.debug(f"LIST KWARGS: {kwargs}")
        cursor = self._conn["user"].find(kwargs)
        users = []
        async for user in cursor:
            user["user_id"] = str(user["_id"])
            user.pop("_id", None)
            users.append(user)
        return users
