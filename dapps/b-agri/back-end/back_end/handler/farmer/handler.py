import pymongo
from bson.objectid import ObjectId
from utils.response import ApiBadRequest, success
from datetime import datetime

from datetime import datetime


class FarmerHandler:
    def __init__(self, database):
        self.__database = database

    async def get_farmers(self, filter_data):
        filter_obj = {}
        if filter_data.get("manager_id"):
            filter_obj["manager_id"] = ObjectId(filter_data["manager_id"])
        farmers = await self.__database.conn.farmer.find(filter_obj, {"phone": 0}).to_list(None)
        for farmer in farmers:
            farmer["farmer_id"] = str(farmer["_id"])
            farmer["manager_id"] = str(farmer["manager_id"])
            farmer.pop('_id')

        return success({
            "farmers": farmers
        })

    async def get_farmer(self, farmer_id):
        farmer = await self.__database.conn.farmer.find_one({
            "_id": ObjectId(farmer_id)
        })
        if farmer is None:
            return ApiBadRequest("Farmer not found")
        manager = await self.__database.conn.user.find_one({
            "_id": farmer["manager_id"],
            "role": "qlv"
        })

        farmer["farmer_id"] = str(farmer["_id"])
        farmer["workdays"] = await self.calcuate_farmer_workday(farmer_id)
        farmer["manager"] = {}
        farmer["manager"]["fullname"] = manager["fullname"]
        farmer["manager"]["id"] = str(manager["_id"])

        tasks = await self.__database.conn.task.find(
            {"farmer_ids": ObjectId(farmer_id)},
            {"_id": 1, "name": 1, "date": 1, "start_time": 1, "end_time": 1}
        ).sort([("date", pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)]).to_list(None)

        for task in tasks:
            task["task_id"] = str(task["_id"])
            task["date"] = task["date"].strftime("%d-%m-%Y")
            task["start_time"] = task["start_time"].strftime("%H:%M")
            task["end_time"] = task["end_time"].strftime("%H:%M")
            task.pop('_id')
        farmer["tasks"] = tasks

        farmer.pop('manager_id')
        farmer.pop('_id')

        return success({
            "farmer": farmer
        })

    async def create_farmer(self, new_farmer):
        new_farmer["manager_id"] = ObjectId(new_farmer["manager_id"])

        manager = await self.__database.conn.user.find_one({
            "_id": new_farmer["manager_id"],
            "role": "qlv"
        })
        if not manager:
            return ApiBadRequest("Manager not found")

        farmer = await self.__database.conn.farmer.insert_one(new_farmer)
        new_farmer["farmer_id"] = str(farmer.inserted_id)
        new_farmer["manager_id"] = str(new_farmer["manager_id"])
        new_farmer.pop('_id')

        # Create notification
        await self.create_notification(
            str(manager["_id"]), 
            "Tạo nông dân", 
            f"Nông dân {new_farmer['fullname']} được thêm vào danh sách quản lý của bạn")

        return success({
            "farmer": new_farmer
        })

    async def update_farmer(self, farmer_id, update_farmer):
        update_farmer["manager_id"] = ObjectId(update_farmer["manager_id"])
        manager = await self.__database.conn.user.find_one({
            "_id": update_farmer["manager_id"],
            "role": "qlv"
        })
        if not manager:
            return ApiBadRequest("Manager not found")

        updated_farmer = await self.__database.conn.farmer.find_one_and_update(
            {
                "_id": ObjectId(farmer_id)
            },
            {
                "$set": update_farmer
            },
            return_document=True
        )
        if not updated_farmer:
            return ApiBadRequest("Farmer not found")
        updated_farmer["farmer_id"] = str(updated_farmer["_id"])
        updated_farmer.pop('_id')
        updated_farmer.pop('manager_id')

        # Create notification
        await self.create_notification(
            str(manager["_id"]), 
            "Cập nhật nông dân", 
            f"Nông dân {updated_farmer['fullname']} bạn quản lý được cập nhật thông tin")

        return success({
            "updated_farmer": updated_farmer
        })

    async def delete_farmer(self, farmer_id):
        deleted_farmer = await self.__database.conn.farmer.find_one_and_delete(
            {
                "_id": ObjectId(farmer_id)
            }
        )
        if not deleted_farmer:
            return ApiBadRequest("Farmer not found")

        # Create notification
        await self.create_notification(
            str(deleted_farmer["manager_id"]), 
            "Xóa nông dân", 
            f"Nông dân {deleted_farmer['fullname']} bạn quản lý đã được xóa khỏi danh sách")
        
        return success({
            "deleted_id": farmer_id
        })

    async def calcuate_farmer_workday(self, farmer_id):
        first_date_of_month = datetime.now().replace(day=1)
        distinct_days = await self.__database.conn.task.distinct(
            "date",
            {
                "farmer_ids": ObjectId(farmer_id),
                "date": {
                    "$gte": first_date_of_month
                }
            }
        )
        return len(distinct_days)

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

