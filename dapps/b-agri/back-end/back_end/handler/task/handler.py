from datetime import datetime

from bson.objectid import ObjectId
import pymongo
from utils.logging import get_logger
from utils.response import ApiBadRequest, ApiNotFound, success

_LOGGER = get_logger(__name__)


class TaskHandler:
    def __init__(self, database, sdk_handler):
        self.__database = database
        self.__sdk_handler = sdk_handler

    async def get_tasks(self):
        tasks = await self.__database.conn.task.find(
            {},
            {"_id": 1, "name": 1, "date": 1, "start_time": 1, "end_time": 1}
        ).sort([("date", pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)]).to_list(None)

        self.post_process_task_docs_list(tasks)

        return success({
            "tasks": tasks
        })

    async def get_task(self, task_id):
        task = await self.__database.conn.task.find_one({"_id": ObjectId(task_id)})
        if not task:
            return ApiNotFound("Task not found")
        task["task_id"] = str(task["_id"])

        farmers = await self.__database.conn.farmer.find(
            {"_id": {"$in": task["farmer_ids"]}},
            {"_id": 1, "fullname": 1}
        ).to_list(length=None)
        for farmer in farmers:
            farmer["farmer_id"] = str(farmer["_id"])
            del farmer["_id"]
        task["farmers"] = farmers
        task["season_id"] = str(task["season_id"])
        task["manager_id"] = str(task["manager_id"])
        task["start_time"] = datetime.strftime(
            task["start_time"], '%Y-%m-%d %H:%M')
        task["end_time"] = datetime.strftime(
            task["end_time"], '%Y-%m-%d %H:%M')
        task["date"] = datetime.strftime(task["date"], '%Y-%m-%d')
        if task.get("items") is None:
            task["items"] = ""
        if task.get("step_id") is None:
            task["step"] = None
        else:
            step = await self.__database.conn.step.find_one({"_id": ObjectId(task["step_id"])}, {"_id": 1, "name": 1})
            if step is None:
                task["step"] = None
            else:
                task["step"] = {
                    "step_id": str(step["_id"]),
                    "name": step["name"]
                }
            task.pop("step_id")

        task.pop("_id")
        task.pop("farmer_ids")

        bc_task = self.__sdk_handler.get_task(task_id)
        print("sdk data: ", bc_task)
        return success({
            "task": task
        })

    async def create_task(self, new_task):
        new_task["farmer_ids"] = list(map(ObjectId, new_task["farmer_ids"]))
        new_task["date"] = datetime.strptime(new_task["date"], '%Y-%m-%d')
        new_task["start_time"] = datetime.strptime(
            new_task["start_time"], '%Y-%m-%d %H:%M')
        new_task["end_time"] = datetime.strptime(
            new_task["end_time"], '%Y-%m-%d %H:%M')
        new_task["season_id"] = ObjectId(new_task["season_id"])

        new_task["step_id"] = ObjectId(new_task["step_id"])
        try:
            await self.__database.conn.task.insert_one(new_task)
        except Exception as e:
            _LOGGER.error(e)
            return ApiBadRequest("Invalid farmer task")

        new_task["task_id"] = str(new_task["_id"])
        farmers = await self.__database.conn.farmer.find(
            {"_id": {"$in": new_task["farmer_ids"]}},
            {"_id": 1, "fullname": 1}
        ).to_list(length=None)
        for farmer in farmers:
            farmer["farmer_id"] = str(farmer["_id"])
            del farmer["_id"]
        new_task["farmer_ids"] = list(map(str, new_task["farmer_ids"]))
        new_task["season_id"] = str(new_task["season_id"])
        new_task["manager_id"] = str(new_task["manager_id"])
        new_task["start_time"] = datetime.strftime(
            new_task["start_time"], '%Y-%m-%d %H:%M')
        new_task["end_time"] = datetime.strftime(
            new_task["end_time"], '%Y-%m-%d %H:%M')
        new_task["date"] = datetime.strftime(new_task["date"], '%Y-%m-%d')
        if new_task.get("step_id") is None:
            new_task["step"] = None
        else:
            step = await self.__database.conn.step.find_one({"_id": ObjectId(new_task["step_id"])}, {"_id": 1, "name": 1})
            if step is None:
                new_task["step"] = None
            else:
                new_task["step"] = {
                    "step_id": str(step["_id"]),
                    "name": step["name"]
                }
                new_task.pop("step_id")

        new_task["farmers"] = farmers
        new_task.pop("_id")

        txn = self.__sdk_handler.create_task(new_task["task_id"], new_task["name"], new_task["description"], new_task["date"], new_task["start_time"], new_task["end_time"], "", new_task["season_id"], new_task["farmer_ids"])
        print("txn task: ", txn)

        season = await self.__database.conn.season.find_one({
            "_id": ObjectId(new_task["season_id"])
        }) 

        garden = await self.__database.conn.garden.find_one({
            "_id": season["garden_id"]
        }) 

        admins = await self.__database.conn.user.find({"role": "ktv"}).to_list(None)


        for admin in admins:
            await self.create_notification(
                    str(admin["_id"]), 
                    "Tạo công việc", 
                    f"Công việc mới {new_task['name']} đã được tạo trên vườn {garden['name']}")
        return success({
            "task": new_task
        })

    async def update_task(self, task_id, update_task):
        update_task["farmer_ids"] = list(
            map(ObjectId, update_task["farmer_ids"]))
        update_task["season_id"] = ObjectId(update_task["season_id"])
        update_task["manager_id"] = ObjectId(update_task["manager_id"])
        update_task["date"] = datetime.strptime(
            update_task["date"], '%Y-%m-%d')
        update_task["start_time"] = datetime.strptime(
            update_task["start_time"], '%Y-%m-%d %H:%M')
        update_task["end_time"] = datetime.strptime(
            update_task["end_time"], '%Y-%m-%d %H:%M')

        try:
            await self.__database.conn.task.find_one_and_update(
                {"_id": ObjectId(task_id)},
                {"$set": update_task}
            )
        except Exception as e:
            _LOGGER.error(e)
            return ApiBadRequest("Invalid farmer task")

        farmers = await self.__database.conn.farmer.find(
            {"_id": {"$in": update_task["farmer_ids"]}},
            {"_id": 1, "fullname": 1}
        ).to_list(length=None)
        for farmer in farmers:
            farmer["farmer_id"] = str(farmer["_id"])
            del farmer["_id"]

        update_task["farmers"] = farmers
        update_task["task_id"] = task_id
        update_task["farmer_ids"] = list(map(str, update_task["farmer_ids"]))
        update_task["season_id"] = str(update_task["season_id"])
        update_task["manager_id"] = str(update_task["manager_id"])
        update_task["start_time"] = datetime.strftime(
            update_task["start_time"], '%Y-%m-%d %H:%M')
        update_task["end_time"] = datetime.strftime(
            update_task["end_time"], '%Y-%m-%d %H:%M')
        update_task["date"] = datetime.strftime(
            update_task["date"], '%Y-%m-%d')


        if update_task.get("step_id") is None:
            update_task["step"] = None
        else:
            step = await self.__database.conn.step.find_one({"_id": ObjectId(update_task["step_id"])}, {"_id": 1, "name": 1})
            if step is None:
                update_task["step"] = None
            else:
                update_task["step"] = {
                    "step_id": str(step["_id"]),
                    "name": step["name"]
                }
            update_task.pop("step_id")
        season = await self.__database.conn.season.find_one({
            "_id": ObjectId(update_task["season_id"])
        }) 

        garden = await self.__database.conn.garden.find_one({
            "_id": season["garden_id"]
        }) 

        admins = await self.__database.conn.user.find({"role": "ktv"}).to_list(None)


        for admin in admins:
            await self.create_notification(
                    str(admin["_id"]), 
                    "Cập nhật công việc", 
                    f"Công việc {update_task['name']} đã được cập nhật trên vườn {garden['name']}")

        return success({
            "updated_task": update_task
        })

    async def delete_task(self, task_id):
        deleted_task = await self.__database.conn.task.find_one_and_delete(
            {
                "_id": ObjectId(task_id)
            })
        if not deleted_task:
            return ApiNotFound("Task not found")
        
        season = await self.__database.conn.season.find_one({
            "_id": ObjectId(deleted_task["season_id"])
        }) 

        garden = await self.__database.conn.garden.find_one({
            "_id": season["garden_id"]
        }) 

        admins = await self.__database.conn.user.find({"role": "ktv"}).to_list(None)


        for admin in admins:
            await self.create_notification(
                    str(admin["_id"]), 
                    "Cập nhật công việc", 
                    f"Công việc {deleted_task['name']} đã được xóa trên vườn {garden['name']}")

        return success({
            "deleted_id": task_id
        })

    def post_process_task_docs_list(self, tasks):
        for task in tasks:
            task["task_id"] = str(task["_id"])
            task["date"] = task["date"].strftime("%d-%m-%Y")
            task["start_time"] = task["start_time"].strftime("%H:%M")
            task["end_time"] = task["end_time"].strftime("%H:%M")
            task.pop('_id')

    async def get_tasks_by_season(self, season_id):
        tasks = await self.__database.conn.task.find(
            {"season_id": ObjectId(season_id)},
            {"_id": 1, "name": 1, "date": 1, "start_time": 1, "end_time": 1}
        ).sort([("date", pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)]).to_list(None)

        self.post_process_task_docs_list(tasks)

        return success({
            "tasks": tasks
        })

    async def get_season_tasks_by_date(self, season_id, date):
        tasks = await self.__database.conn.task.find(
            {
                "date": datetime.strptime(date, "%d-%m-%Y"),
                "season_id": ObjectId(season_id),
            },
            {"_id": 1, "name": 1, "date": 1, "start_time": 1, "end_time": 1}
        ).sort([("date", pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)]).to_list(None)

        self.post_process_task_docs_list(tasks)

        return success({
            "tasks": tasks
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
