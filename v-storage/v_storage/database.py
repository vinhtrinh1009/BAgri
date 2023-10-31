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
                if attempt == retries-1:
                    _LOGGER.error("Cannot connect to the database")
                    raise ServerSelectionTimeoutError
                else:
                    _LOGGER.debug("Database connection failed")
                    await asyncio.sleep(delay)

    ##############
    ### Folder ###
    ##############
    async def get_folders(self, folder_filter):
        tmp_folders = self._conn["folders"].find(folder_filter)
        folders = []
        async for folder in tmp_folders:
            folder["folder_id"] = str(folder["_id"])
            folder.pop("_id", None)
            folders.append(folder)
        return folders
    
    async def create_folder(self, new_folder):
        result = await self._conn["folders"].insert_one(new_folder)
        folder_id = str(result.inserted_id)
        return folder_id

    async def update_folder(self, folder_filter, modification):
        updated_folder = await self._conn["folders"].find_one_and_update(folder_filter,
                                                                        {'$set': modification},
                                                                        return_document=ReturnDocument.AFTER)
        updated_folder["folder_id"] = str(updated_folder["_id"])
        updated_folder.pop("_id", None)
        return updated_folder

    async def update_folders(self, folder_filter, modification):
        await self._conn["folders"].update_many(folder_filter, {'$set': modification})

    async def delete_folder(self, folder_filter):
        result = await self._conn["folders"].delete_many(folder_filter)
        return {
            "number_deleted_folders": result.deleted_count
        }

    ############
    ### File ###
    ############
    async def get_files(self, file_filter):
        tmp_files = self._conn["files"].find(file_filter)
        files = []
        async for file in tmp_files:
            file["file_id"] = str(file["_id"])
            file.pop("_id", None)
            files.append(file)
        return files

    async def create_file(self, new_file):
        result = await self._conn["files"].insert_one(new_file)
        file_id = str(result.inserted_id)
        return file_id

    async def update_file(self, file_filter, modification):
        updated_file = await self._conn["files"].find_one_and_update(file_filter,
                                                                    {'$set': modification},
                                                                    return_document=ReturnDocument.AFTER)
        updated_file["file_id"] = str(updated_file["_id"])
        updated_file.pop("_id", None)
        return updated_file

    async def update_files(self, file_filter, modification):
        await self._conn["files"].update_many(file_filter, {'$set': modification})

    async def delete_file(self, file_filter):
        result = await self._conn["files"].delete_many(file_filter)
        return {
            "number_deleted_files": result.deleted_count
        }

    ##################
    ### Activities ###
    ##################
    async def get_activities(self, activity_filter):
        tmp_activities = self._conn["activities"].find(activity_filter).sort("datetime").limit(20)
        activities = []
        async for activity in tmp_activities:
            activity["activitie_id"] = str(activity["_id"])
            activity.pop("_id", None)
            activities.append(activity)
        return activities

    async def create_activity(self, new_activity):
        result = await self._conn["activities"].insert_one(new_activity)
        activity_id = str(result.inserted_id)
        return activity_id

    async def update_activity(self, activity_id, modification):
        activity_filter = {
            "_id": ObjectId(activity_id)
        }
        updated_activity = await self._conn["activities"].find_one_and_update(activity_filter,
                                                                    {'$set': modification},
                                                                    return_document=ReturnDocument.AFTER)
        updated_activity["activity_id"] = str(updated_activity["_id"])
        updated_activity.pop("_id", None)
        return updated_activity

    async def delete_activity(self, activity_filter):
        result = await self._conn["activities"].delete_many(activity_filter)
        return {
            "number_deleted_activities": result.deleted_count
        }