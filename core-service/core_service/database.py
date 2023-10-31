import asyncio
import resource
import motor.motor_asyncio as aiomotor
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError

from utils.logging import get_logger

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
                _LOGGER.info(f"List collection: {await self._conn.list_collection_names()}")
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
        cursor = self._conn["network"].find(kwargs)
        networks = []
        async for network in cursor:
            network["network_id"] = str(network["_id"])
            network.pop("_id", None)
            networks.append(network)
        return networks

    async def update_network(self, user_id, network_id, modification=None, unset=None):
        network_filter = {
            "_id": ObjectId(network_id),
            "user_id": user_id
        }
        update = {}
        if modification:
            update['$set'] = modification
        if unset:
            update['$unset'] = unset
        updated_network = await self._conn["network"].find_one_and_update(network_filter,
                                                                          update=update,
                                                                          return_document=ReturnDocument.AFTER)
        updated_network["network_id"] = str(updated_network["_id"])
        updated_network.pop("_id", None)

        return updated_network

    async def delete_network(self, network_id, user_id):
        network_filter = {
            "_id": ObjectId(network_id),
            "user_id": user_id
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
            resource["resource_id"] = str(resource["_id"])
            resource.pop("_id", None)
            resources.append(resource)
        return resources       

    async def update_resource(self, resource_id, user_id, modification=None, unset=None):
        resource_filter = {
            "_id": ObjectId(resource_id),
            "user_id": user_id
        }
        _LOGGER.debug(f"Update resource with {resource_filter}")
        update = {}
        if modification:
            update['$set'] = modification
        if unset:
            update['$unset'] = unset
        update_resource = await self._conn["resource"].find_one_and_update(resource_filter,
                                                                    update=update,
                                                                    return_document=ReturnDocument.AFTER)
        if update_resource and update_resource['_id']:
            _LOGGER.debug(f"{update_resource['_id']} Updated")
            update_resource["resource_id"] = str(update_resource["_id"])
            update_resource.pop("_id", None)
        return update_resource

    async def delete_resource(self, resource_id=None, user_id=None, network_id=None):
        resource_filter = {}
        if resource_id:
            resource_filter["_id"] = ObjectId(resource_id)
        if user_id:
            resource_filter["user_id"] = user_id
        if network_id:
            resource_filter["network_id"] = network_id
        result = await self._conn["dapp"].delete_many(resource_filter)
        return {
            "number_deleted_network": result.deleted_count
        }

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

    async def update_dapp(self, dapp_id, user_id, modification=None, unset=None):
        dapp_filter = {
            "_id": ObjectId(dapp_id),
            "user_id": user_id
        }
        update = {}
        if modification:
            update['$set'] = modification
        if unset:
            update['$unset'] = unset
        updated_dapp = await self._conn["dapp"].find_one_and_update(filter=dapp_filter,
                                                                    update=update,
                                                                    return_document=ReturnDocument.AFTER)
        if updated_dapp and updated_dapp['_id']:
            updated_dapp["dapp_id"] = str(updated_dapp["_id"])
            updated_dapp.pop("_id", None)
        return updated_dapp

    async def delete_dapp(self, dapp_id=None, user_id=None, network_id=None):
        dapp_filter = {}
        if dapp_id:
            dapp_filter["_id"] = ObjectId(dapp_id)
        if user_id:
            dapp_filter["user_id"] = user_id
        if network_id:
            dapp_filter["network_id"] = network_id
        result = await self._conn["dapp"].delete_many(dapp_filter)
        return {
            "number_deleted_network": result.deleted_count
        }

    async def update_multi_dapp(self, network_id, user_id, modification=None, unset=None):
        dapp_filter = {
            "network_id": network_id,
            "user_id": user_id
        }
        update = {}
        if modification:
            update['$set'] = modification
        if unset:
            update['$unset'] = unset
        updated_dapps = await self._conn["dapp"].update_many(filter=dapp_filter,
                                                            update=update)
        return updated_dapps
