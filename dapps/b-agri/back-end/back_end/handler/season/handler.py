from datetime import datetime
import json
import os
import aiohttp_jinja2

from settings import config
import qrcode
from bson.objectid import ObjectId
import pymongo
from utils.update_stages import get_process_stages, get_stage, get_trees
from utils.logging import get_logger
from utils.response import (ApiBadRequest, ApiInternalError, ApiNotFound,
                            success)

from sdk.py_handler import Handler as SdkHandler
_LOGGER = get_logger(__name__)


class SeasonHandler:
    def __init__(self, database, sdk_handler):
        self.__database = database
        self.__sdk_handler = sdk_handler

    async def get_seasons(self):
        seasons = await self.__database.conn.season.find(
            {}, {"_id": 1, "name": 1, "garden_id": 1, "process.name": 1, "status": 1}
        ).sort([("start_date", pymongo.DESCENDING)]).to_list(length=None)

        for season in seasons:
            season["season_id"] = str(season["_id"])
            del season["_id"]

            process_doc = await self.__database.conn.process.find_one({"season_id": ObjectId(season["season_id"])})
            if process_doc is not None:
                season["process"] = {}
                season["process"]["process_id"] = str(process_doc["_id"])
                season["process"]["name"] = process_doc["name"]
            else:
                season["garden"] = {}

            garden = await self.__database.conn.garden.find_one({"_id": ObjectId(season["garden_id"])})
            if garden:
                season["garden"] = {}
                season["garden"]["garden_id"] = str(garden["_id"])
                season["garden"]["name"] = garden["name"]
            else:
                season["garden"] = {}

            season.pop("garden_id")
        return success({
            "seasons": seasons
        })

    async def get_season(self, season_id):
        season_doc = await self.__database.conn.season.find_one({"_id": ObjectId(season_id)})
        if not season_doc:
            return ApiNotFound("Season not found")

        response_data = {}
        response_data["name"] = season_doc["name"]
        response_data["start_date"] = season_doc["start_date"].strftime(
            '%d-%m-%Y')
        response_data["end_date"] = season_doc["end_date"].strftime('%d-%m-%Y')
        response_data["status"] = season_doc["status"]
        response_data["season_id"] = str(season_doc["_id"])
        response_data["process"] = {}
        response_data["tree"] = {}

        process_doc = await self.__database.conn.process.find_one({"season_id": ObjectId(season_doc["_id"])})
        trees = await get_trees(self.__database, process_doc["tree_ids"])
        response_data["process"]["trees"] = trees
        stages = await get_process_stages(self.__database, process_doc["_id"])

        response_data["process"]["name"] = process_doc["name"]
        response_data["process"]["process_id"] = str(process_doc["_id"])
        response_data["process"]["stages"] = stages
        response_data["process"]["template_process_id"] = str(
            process_doc["template_process_id"])

        tree = await self.__database.conn.tree.find_one({"_id": ObjectId(season_doc["tree_id"])})
        response_data["tree"]["id"] = str(tree["_id"])
        response_data["tree"]["name"] = tree["name"]

        garden = await self.__database.conn.garden.find_one({"_id": ObjectId(season_doc["garden_id"])})
        response_data["garden"] = {}
        response_data["garden"]["id"] = str(garden["_id"])
        response_data["garden"]["name"] = garden["name"]

        # season_sdk = self.__sdk_handler.get_season(str(season_id))
        # print("sdk get ve", season_sdk)

        return success({
            "season": response_data
        })

    async def create_season(self, new_season):
        new_season["garden_id"] = ObjectId(new_season["garden_id"])
        new_season["tree_id"] = ObjectId(new_season["tree_id"])
        new_season["start_date"] = datetime.strptime(
            new_season["start_date"], '%d-%m-%Y')
        new_season["end_date"] = datetime.strptime(
            new_season["end_date"], '%d-%m-%Y')
        new_season["status"] = new_season.get("status")

        response_data = {}
        response_data["start_date"] = new_season["start_date"]
        response_data["end_date"] = new_season["end_date"]
        response_data["status"] = new_season["status"]
        response_data["process"] = {}

        template_process = await self.__database.conn.process.find_one({"_id": ObjectId(new_season["process_id"])})
        if not template_process:
            return ApiNotFound("Process not found")

        tree = await self.__database.conn.tree.find_one({"_id": ObjectId(new_season["tree_id"])})
        if not tree:
            return ApiNotFound("Tree not found")

        template_process["template_process_id"] = ObjectId(
            template_process["_id"])
        if new_season["tree_id"] not in template_process["tree_ids"]:
            return ApiBadRequest("Tree not found in process")
        trees = await get_trees(self.__database, template_process["tree_ids"])
        response_data["process"]["trees"] = trees
        new_season["process_id"] = ObjectId(new_season["process_id"])
        inserted_season = await self.__database.conn.season.insert_one(new_season)

        inserted_process = await self.__database.conn.process.insert_one({
            "name": template_process["name"],
            "tree_ids": template_process["tree_ids"],
            "template_process_id": template_process["_id"],
            "season_id": inserted_season.inserted_id,
        })
        stages = []
        # duplicate the stage
        temp_stage_docs = await self.__database.conn.stage.find({"process_id": template_process["_id"]}).to_list(length=None)
        for idx, stage_doc in enumerate(temp_stage_docs):
            # stage["steps"] = []
            new_steps = []
            new_stage = {}
            new_stage["name"] = stage_doc["name"]
            new_stage["template_process_id"] = template_process["_id"]
            new_stage["process_id"] = inserted_process.inserted_id,
            new_stage["idx"] = idx
            inserted_stage = await self.__database.conn.stage.insert_one(new_stage)

            new_stage["stage_id"] = str(new_stage["_id"])
            stages.append({
                "stage_id": str(inserted_stage.inserted_id),
                "steps": new_steps,
                "name": new_stage["name"],
                "template_process_id": str(new_stage["template_process_id"]),
                "process_id": str(inserted_process.inserted_id),
            })
            step_docs = await self.__database.conn.step.find({"stage_id": stage_doc["_id"]}).to_list(length=None)
            for idx, step_doc in enumerate(step_docs):
                new_step = {
                    "name": step_doc["name"],
                    "from_day": step_doc["from_day"],
                    "to_day": step_doc["to_day"],
                    "stage_id": new_stage["_id"],
                    "idx": idx
                }
                await self.__database.conn.step.insert_one(new_step)

                new_step["step_id"] = str(new_step["_id"])
                new_step.pop("_id")
                new_step["stage_id"] = str(new_step["stage_id"])
                new_steps.append(new_step)

        response_data["process"]["stages"] = stages
        response_data["process"]["name"] = template_process["name"]
        response_data["process"]["process_id"] = str(
            inserted_process.inserted_id)
        response_data["process"]["template_process_id"] = str(
            template_process["_id"])
        response_data["name"] = new_season["name"]

        garden = await self.__database.conn.garden.find_one({"_id": ObjectId(new_season["garden_id"])})
        if not garden:
            return ApiNotFound("Garden not found")

        template_process.pop("_id")
        template_process["tree_ids"] = list(
            map(ObjectId, template_process["tree_ids"]))
        template_process["season_id"] = inserted_season.inserted_id

        tree = await self.__database.conn.tree.find_one({"_id": ObjectId(new_season["tree_id"])})
        response_data["tree"] = {}
        response_data["tree"]["id"] = str(tree["_id"])
        response_data["tree"]["name"] = tree["name"]

        response_data["garden"] = {}
        response_data["garden"]["id"] = str(garden["_id"])
        response_data["garden"]["name"] = garden["name"]
        response_data["season_id"] = str(new_season["_id"])

        response_data["start_date"] = new_season["start_date"].strftime(
            '%d-%m-%Y')
        response_data["end_date"] = new_season["end_date"].strftime('%d-%m-%Y')

        # Create notification    
        await self.create_notification(
            garden["manager_id"], 
            "Tạo mùa vụ ", 
            f"Mùa vụ {new_season['name']} đã được tạo trên vườn {garden['name']}"
        )

        return success({
            "season": response_data
        })

    async def update_season(self, season_id, update_season):
        season_doc = await self.__database.conn.season.find_one({"_id": ObjectId(season_id)})
        if not season_doc:
            return ApiNotFound("Không tìm thấy mùa vụ")
        if season_doc["status"] == "done":
            return ApiBadRequest("Không thể sửa mùa vụ đã kết thúc")

        update_season["garden_id"] = ObjectId(update_season["garden_id"])
        update_season["tree_id"] = ObjectId(update_season["tree_id"])
        update_season["start_date"] = datetime.strptime(
            update_season["start_date"], '%d-%m-%Y')
        update_season["end_date"] = datetime.strptime(
            update_season["end_date"], '%d-%m-%Y')
        update_season["status"] = update_season.get("status")

        garden = await self.__database.conn.garden.find_one({"_id": ObjectId(update_season["garden_id"])})
        if not garden:
            return ApiNotFound("Garden not found")

        tree = await self.__database.conn.tree.find_one({"_id": ObjectId(update_season["tree_id"])})
        if not tree:
            return ApiNotFound("Process not found")

        updated_season = await self.__database.conn.season.find_one_and_update(
            {"_id": ObjectId(season_id)},
            {"$set": update_season},
            return_document=True
        )
        if not updated_season:
            return ApiNotFound("Season not found")

        updated_season["season_id"] = str(updated_season["_id"])
        del updated_season["_id"]

        updated_season["tree_id"] = str(updated_season["tree_id"])
        updated_season["garden_id"] = str(updated_season["garden_id"])
        updated_season["start_date"] = updated_season["start_date"].strftime(
            '%d-%m-%Y')
        updated_season["end_date"] = updated_season["end_date"].strftime(
            '%d-%m-%Y')
        
        updated_season.pop("process_id")

        # Create notification    
        await self.create_notification(
            garden["manager_id"], 
            "Cập nhật mùa vụ", 
            f"Mùa vụ {updated_season['name']} đã được cập nhật trên vườn {garden['name']}"
        )

        return success({
            "updated_season": updated_season
        })

    async def delete_season(self, season_id):
        season_doc = await self.__database.conn.season.find_one({"_id": ObjectId(season_id)})
        if not season_doc:
            return ApiNotFound("Mùa vụ không tồn tại")
        if season_doc["status"] == "done":
            return ApiBadRequest("Không thể sửa mùa vụ đã kết thúc")

        deleted_season = await self.__database.conn.season.find_one_and_delete(
            {"_id": ObjectId(season_id)}
        )

        if not deleted_season:
            return ApiNotFound("Season not found")
        
        # Create notification
        garden = await self.__database.conn.garden.find_one({"_id": deleted_season["garden_id"]}) 
        await self.create_notification(
            str(garden["manager_id"]), 
            "Xóa mùa vụ", 
            f"Mùa vụ {deleted_season['name']} tại vườn {garden['name']} đã được xóa"
        )

        return success({
            "deleted_season": str(deleted_season["_id"])
        })

    async def get_season_steps(self, season_id):
        season = await self.__database.conn.season.find_one({"_id": ObjectId(season_id)})
        if season is None:
            return ApiNotFound("Season not found")
        process = await self.__database.conn.process.find_one({"season_id": ObjectId(season_id)})
        if process is None:
            return ApiNotFound("Season process not found")
        stages = await get_process_stages(self.__database, process["_id"])
        steps = get_steps_from_stages(stages)
        steps = [{"step_id": step.get("step_id"),
                  "name": step.get("name")} for step in steps]
        return success({"steps": steps})

    async def get_season_process(self, season_id):
        season = await self.__database.conn.season.find_one(
            {"_id": ObjectId(season_id)},
            {"process": 1}
        )
        if not season:
            return ApiNotFound("Season not found")
        process = season["process"]

        for stage in process["stages"]:
            step_ids = stage["steps"]
            stage["steps"] = []
            for step_id in step_ids:
                step = await self.__database.conn.step.find_one({"_id": ObjectId(step_id)})
                step["step_id"] = str(step["_id"])
                step.pop("_id")
                stage["steps"].append(step)

        trees = await self.__database.conn.tree.find(
            {"_id": {"$in": process["tree_ids"]}}, {"_id": 1, "name": 1}
        ).to_list(length=None)

        process["trees"] = [{
            "tree_id": str(tree["_id"]),
            "name": tree["name"]
        } for tree in trees]
        del process["tree_ids"]
        process["template_process_id"] = str(process["template_process_id"])
        return success({
            "process": process
        })

    async def update_season_process(self, season_id, process):
        season = await self.__database.conn.season.find_one(
            {"_id": ObjectId(season_id)},
            {"process.tree_ids": 0, "process.template_process_id": 0}
        )
        if not season:
            return ApiNotFound("Season not found")
        season["process"] = {}
        season["process"]["name"] = process["name"]
        updated_stages = []
        for stage in process["stages"]:
            for step in stage["steps"]:
                if step.get("step_id") is not None:
                    step_id = step["step_id"]
                    step.pop("step_id")
                    await self.__database.conn.step.find_one_and_update(
                        {"_id": ObjectId(step_id)},
                        {"$set": step}
                    )
                    step["step_id"] = step_id
                else:
                    await self.__database.conn.step.insert_one(step)
                    step["step_id"] = str(step["_id"])
                    step.pop("_id")
            updated_stages.append(
                {"steps": [ObjectId(step["step_id"]) for step in stage["steps"]]})

        # TODO: delete steps that are deleted
        await self.__database.conn.season.find_one_and_update(
            {"_id": ObjectId(season_id)},
            {"$set": {"process.name": process["name"], "process.stages": updated_stages}
             })

        # Create notification   
        garden = await self.__database.conn.garden.find_one(
            {"_id": season["garden_id"]}
        ) 
        await self.create_notification(
            garden["manager_id"], 
            "Cập nhật quy trình của mùa vụ", 
            f"Mùa vụ {season['name']} tại vườn {garden['name']} đã được cập nhật quy trình mới"
        )

        return success({"process": process})

    async def get_current_season_step(self, season_id):
        season = await self.__database.conn.season.find_one({"_id": ObjectId(season_id)})
        if season is None:
            return ApiNotFound("Season not found")
        process = await self.__database.conn.process.find_one({"season_id": ObjectId(season_id)})
        if process is None:
            return ApiNotFound("Season process not found")
        stages = await get_process_stages(self.__database, process["_id"])
        step = get_current_season_step(stages)
        return success({"step": step})

    async def generate_qr_code(self, season_id):
        season = await self.__database.conn.season.find_one({"_id": ObjectId(season_id)})
        if season is None:
            return ApiNotFound("Season not found")

        domain = config.get("domain") or "http://localhost:8080"
        qr_img = qrcode.make(f'{domain}/v1/seasons/network/{season_id}')
        file_path = os.path.join("static", "qr_codes", f'{season_id}.png')
        qr_img.save(file_path)
        return success({
            "qr_code_url": f"{domain}/static/qr_codes/{season_id}.png"
        })

    async def get_season_from_network(self, request, season_id):
        season = self.__sdk_handler.get_season(season_id)
        if season is None:
            return ApiNotFound("Season not found")
        print(season)
        season_data = {}
        season_data["season_id"] = season[0]
        season_data["process"] = json.loads(season[1])
        season_data["start_date"] = season[2]
        season_data["end_date"] = season[3]
        season_data["season_id"] = season[4]
        season_data["tree_id"] = season[5]
        season_data["task_ids"] = season[6]

        tasks = []
        task_ids = season_data["task_ids"]
        for task_id in task_ids:
            task = self.__sdk_handler.get_task(task_id)
            tasks.append(task)
        season_data["tasks"] = tasks
        response = aiohttp_jinja2.render_template("season-detail.html", request,
                                          context=season_data)
        return response

    async def create_notification(self, user_id, title, description):
        current_time = datetime.now()
        new_notification = {
            "user_id": user_id,
            "title": title,
            "description": description,
            "seen": False,
            "created_at": current_time
        }
                    
        await self.__database.conn.notification.insert_one(new_notification)

def check_season_completed(stages):
    """
    check is the season is completed/done based on its stages
    """
    for stage in stages:
        for step in stage.get("steps"):
            if step.get("actual_day") is None:
                return False
    return True


def add(x, y):
    return x + y


def get_current_season_step(stages):
    return_step = None
    for stage in stages:
        for step in stage.get("steps"):
            return_step = step
            if step.get("actual_day") is None:
                return step
    return return_step


def get_steps_from_stages(stages):
    steps = []
    for stage in stages:
        steps += stage.get("steps")
    return steps


async def save_season_to_blockchain(db, sdk_handler: SdkHandler, season_id):
    _LOGGER.info(f"Save data to blockchain {season_id}")
    season_doc = await db.conn.season.find_one({"_id": ObjectId(season_id)})
    if not season_doc:
        return None

    tasks = await db.conn.task.find(
        {"season_id": ObjectId(season_id)},
        {"_id": 1, }
    ).sort([("date", pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)]).to_list(None)
    task_ids = [str(task['_id']) for task in tasks]

    process_doc = await db.conn.process.find_one({"season_id": ObjectId(season_doc["_id"])})
    if not process_doc:
        return None

    stages = await get_process_stages(db, process_doc["_id"])
    process = {}
    process["name"] = process_doc["name"]
    process["stages"] = stages
    process_str = json.dumps(process)

    start_date = datetime.strftime(season_doc["start_date"], "%d-%m-%Y")
    end_date = datetime.strftime(season_doc["end_date"], "%d-%m-%Y")

    txn = sdk_handler.create_season(
            str(season_id), process_str, start_date, end_date, str(season_doc["tree_id"]),
            str(season_doc["garden_id"]), task_ids)
    _LOGGER.info(f"Transaction ID: {txn}")
