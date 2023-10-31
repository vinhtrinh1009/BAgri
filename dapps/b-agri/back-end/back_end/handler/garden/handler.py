from bson.errors import InvalidId
from bson.objectid import ObjectId
from utils.logging import get_logger
from utils.response import (ApiBadRequest, ApiInternalError, ApiNotFound,
                            success)
import pymongo
from datetime import datetime

_LOGGER = get_logger(__name__)


class GardenHandler:
    def __init__(self, database):
        self.__database = database

    async def get_gardens(self, filter_data):
        filter_obj = {}
        if filter_data.get("manager_id"):
            filter_obj["manager_id"] = ObjectId(filter_data["manager_id"])
        gardens = await self.__database.conn.garden.find(filter_obj, {"manager_id": 0}).to_list(length=None)
        for garden in gardens:
            garden['garden_id'] = str(garden['_id'])

            seasons = await self.__database.conn.season.find(
                {"garden_id": ObjectId(garden['_id'])},
                {"_id": 1, "name": 1, "status": 1, "start_date": 1, "end_date": 1}
            ).sort([("start_date", pymongo.DESCENDING)]).to_list(length=1)
            if len(seasons) == 1:
                season = seasons[0]
                process_doc = await self.__database.conn.process.find_one({"season_id": ObjectId(season["_id"])})
                if process_doc is not None:
                    garden["process"] = {
                        "process_id": str(process_doc["_id"]),
                        "name": process_doc['name']
                    }
                    garden["process_name"] = process_doc["name"]
                else:
                    garden["process"] = {}
                    garden["process_name"] = ""
                garden["season"] = {
                    "season_id": str(season["_id"]),
                    "name": season["name"]
                }
            else:
                garden["process_name"] = ""
                garden["season"] = {}
            del garden['_id']

        return success({
            "gardens": gardens
        })

    async def get_garden(self, garden_id):
        try:
            garden = await self.__database.conn.garden.find_one({"_id": ObjectId(garden_id)})
        except InvalidId:
            return ApiNotFound("Garden not found")
        if not garden:
            return ApiNotFound("Garden not found")
        manager = await self.__database.conn.user.find_one(
            {"_id": ObjectId(garden["manager_id"]), "role": "qlv"})
        if not manager:
            return ApiBadRequest("Garden not found")

        garden["manager"] = {
            "manager_id": str(manager["_id"]),
            "name": manager["fullname"]
        }
        garden.pop("manager_id")
        garden["garden_id"] = str(garden["_id"])
        del garden["_id"]

        seasons = await self.__database.conn.season.find(
            {"garden_id": ObjectId(garden_id)},
            {"_id": 1, "name": 1, "status": 1, "start_date": 1, "end_date": 1}
        ).sort([("start_date", pymongo.DESCENDING)]).to_list(length=None)

        for season in seasons:
            season["season_id"] = str(season["_id"])
            season["start_date"] = datetime.strftime(
                season["start_date"], '%Y-%m-%d')
            season["end_date"] = datetime.strftime(
                season["end_date"], '%Y-%m-%d')
            del season["_id"]
        garden["seasons"] = seasons

        return success({
            "garden": garden
        })

    async def create_garden(self, new_garden):
        new_garden["area"] = int(new_garden["area"])

        if new_garden["area"] <= 0:
            return ApiBadRequest("Area must be greater than 0")

        try:
            manager = await self.__database.conn.user.find_one(
                {"_id": ObjectId(new_garden["manager_id"]), "role": "qlv"})
            if not manager:
                return ApiBadRequest("Manager not found")
            new_garden["manager_id"] = ObjectId(new_garden["manager_id"])
            await self.__database.conn.garden.insert_one(new_garden)

            new_garden["garden_id"] = str(new_garden["_id"])
            new_garden["manager"] = {
                "manager_id": str(new_garden["manager_id"]),
                "name": manager["fullname"]
            }
            new_garden.pop("_id")
            new_garden.pop("manager_id")

            # Create notification
            await self.create_notification(
                str(manager["_id"]), 
                "Tạo vườn", 
                "Bạn vừa được thêm vào quản lý vườn :" + new_garden["name"])

            return success({
                "garden": new_garden
            })
        except Exception as e:
            _LOGGER.error(e)
            return ApiInternalError("Internal error")

    async def update_garden(self, garden_id, update_garden):
        update_garden["area"] = int(update_garden["area"])
        if update_garden["area"] <= 0:
            return ApiBadRequest("Area must be greater than 0")

        manager = await self.__database.conn.user.find_one(
            {"_id": ObjectId(update_garden["manager_id"]), "role": "qlv"})
        if not manager:
            return ApiBadRequest("Manager not found")

        update_garden["manager_id"] = ObjectId(update_garden["manager_id"])
        updated_garden = await self.__database.conn.garden.find_one_and_update(
            {"_id": ObjectId(garden_id)},
            {"$set": update_garden},
            return_document=True
        )
        if not updated_garden:
            return ApiNotFound("Garden not found")

        updated_garden["manager"] = {
            "manager_id": str(manager["_id"]),
            "name": manager["fullname"]
        }
        updated_garden.pop("manager_id")

        updated_garden = dict(updated_garden)
        updated_garden["garden_id"] = str(updated_garden["_id"])
        del updated_garden["_id"]

        print(updated_garden)

        await self.create_notification(
            str(manager["_id"]), 
            "Cập nhật vườn", 
            f"Một vườn bạn quản lý {update_garden['name']} đã được cập nhật")


        return success({
            "updated_garden": updated_garden

        })

    async def delete_garden(self, garden_id):
        try:    
            deleted_garden = await self.__database.conn.garden.find_one_and_delete(
                {"_id": ObjectId(garden_id)}
            )
            
            # Create notification 
            if deleted_garden:        
                await self.create_notification(
                    str(deleted_garden["manager_id"]), 
                    "Xóa vườn", 
                    f"Một vườn bạn quản lý {deleted_garden['name']} đã được xóa ")

        except InvalidId:
            return ApiNotFound("Garden not found")

        if not deleted_garden: 
            return ApiNotFound("Garden not found")

        return success({
            "garden_id": garden_id
        })

    async def create_notification(self, user_id, title, description):
        now = datetime.now()
        current_time = datetime.timestamp(now)

        new_notification = {
            "user_id": user_id,
            "title": title,
            "description": description,
            "seen": False, 
            "created_at": current_time
        }                    
        await self.__database.conn.notification.insert_one(new_notification)
