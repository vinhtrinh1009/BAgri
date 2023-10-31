from bson.objectid import ObjectId
from utils.response import ApiNotFound, success, ApiBadRequest, ApiInternalError
from utils.logging import get_logger

_LOGGER = get_logger(__name__)

class StepHandler:
    def __init__(self, database):
        self.__database = database

    async def get_steps(self, filter_data):
        filter_obj = {}
        if filter_data.get("season_id"):
            season_doc = await self.__database.conn.season.find_one({"_id": ObjectId(filter_data["season_id"])})
            if not season_doc:
                return ApiNotFound("Season not found")
            process_doc = await self.__database.conn.process.find_one({"season_id": ObjectId(season_doc["_id"])})
            if process_doc is None:
                return ApiNotFound("process not found")

            stage_docs = await self.__database.conn.stage.find({"process_id": ObjectId(process_doc["_id"])}).to_list(length=None)
            stage_ids = [stage_doc["_id"] for stage_doc in stage_docs]
            filter_obj["stage_id"] = { "$in" :stage_ids }

        steps = await self.__database.conn.step.find(filter_obj, {"_id": 1, "name": 1}).to_list(None)
        for step in steps:
            step["step_id"] = str(step["_id"])
            step.pop('_id')

        return success({
            "steps": steps
        })
