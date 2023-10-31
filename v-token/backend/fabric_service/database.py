import os
import asyncio
import motor.motor_asyncio as aiomotor
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError
from fabric_service.logging_config import get_logger

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
                collections_name = await self._conn.list_collection_names()
                _LOGGER.info(f"List collection: {collections_name}")
                _LOGGER.info("Successfully connected to the database")
                return
            except ServerSelectionTimeoutError:
                if attempt == retries - 1:
                    _LOGGER.error("Cannot connect to the database")
                    raise ServerSelectionTimeoutError
                else:
                    _LOGGER.debug("Database connection failed")
                    await asyncio.sleep(delay)

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

    async def create_dapp(self, new_dapp):
        result = await self._conn["dapp"].insert_one(new_dapp)
        dapp_id = str(result.inserted_id)
        return dapp_id
    
    async def get_dapps(self, **kwargs):
        if "dapp_id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs["dapp_id"])
            del kwargs["dapp_id"]
        cursor = self._conn["dapp"].find(kwargs)
        dapps = []
        async for dapp in cursor:
            dapp["dapp_id"] = str(dapp["_id"])
            dapp.pop("_id", None)
            dapps.append(dapp)
        return dapps