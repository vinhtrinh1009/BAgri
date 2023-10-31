from bson.objectid import ObjectId
from handler.season.handler import check_season_completed, save_season_to_blockchain
from utils.update_stages import get_process_stages, get_stage, get_trees, update_stage
from utils.logging import get_logger
from utils.response import ApiBadRequest, ApiInternalError, ApiNotFound, success

class ProcessHandler:
    def __init__(self, database, sdk_handler):
        self.__database = database
        self.__sdk_handler = sdk_handler

    async def get_processes_by_tree(self, tree_id):
        processes = await self.__database.conn.process.find(
            {"template_process_id": {"$exists": False}, "tree_ids": ObjectId(tree_id)}, {"_id": 1, "name": 1, "tree_ids": 1}
        ).to_list(length=None)

        for process in processes:
            process["process_id"] = str(process["_id"])
            del process["_id"]

            # get trees that applied to this process
            # if this request is slow (maybe not), we can query all trees in
            # one query
            trees = await self.__database.conn.tree.find(
                {"_id": {"$in": process["tree_ids"]}}, {"_id": 1, "name": 1}
            ).to_list(length=None)

            process["trees"] = [{
                "tree_id": str(tree["_id"]),
                "name": tree["name"]
            } for tree in trees]
            del process["tree_ids"]

        return success({
            "processes": processes
        })

    async def get_processes(self):
        processes = await self.__database.conn.process.find(
            {"template_process_id": {"$exists": False}}, {"_id": 1, "name": 1, "tree_ids": 1}
        ).to_list(length=None)

        for process in processes:
            process["process_id"] = str(process["_id"])
            del process["_id"]

            # get trees that applied to this process
            # if this request is slow (maybe not), we can query all trees in
            # one query
            trees = await self.__database.conn.tree.find(
                {"_id": {"$in": process["tree_ids"]}}, {"_id": 1, "name": 1}
            ).to_list(length=None)

            process["trees"] = [{
                "tree_id": str(tree["_id"]),
                "name": tree["name"]
            } for tree in trees]
            del process["tree_ids"]

        return success({
            "processes": processes
        })

    async def get_process(self, process_id):
        process_doc = await self.__database.conn.process.find_one({"_id": ObjectId(process_id)})

        if process_doc is None:
            return ApiBadRequest("Process not found")

        trees = await get_trees(self.__database, process_doc["tree_ids"])
        process_doc["trees"] = trees
        del process_doc["tree_ids"]
        stages = await get_process_stages(self.__database, process_doc["_id"])
        res_process = {
            "process_id": str(process_doc["_id"]),
            "name": process_doc["name"],
            "stages": stages,
            "trees": trees
        }

        return success({
            "process": res_process
        })

    async def create_process(self, new_process):
        new_stages = []
        new_stage_ids = []
        new_process["tree_ids"] = [
            ObjectId(tree_id) for tree_id in new_process["tree_ids"]]
        create_process_data = {
            "name": new_process["name"],
            "tree_ids": new_process["tree_ids"],
        }
        process = await self.__database.conn.process.insert_one(create_process_data)
        for idx, stage in enumerate(new_process["stages"]):
            stage["idx"] = idx
            stage["process_id"] = process.inserted_id
            new_stage = await update_stage(self.__database, stage)
            new_stage.pop("_id")
            new_stage_ids.append(ObjectId(new_stage["stage_id"]))
            new_stages.append(
                {
                    "stage_id": new_stage["stage_id"],
                    "process_id": str(new_stage["process_id"]),
                    "name": new_stage["name"],
                    "steps": new_stage["steps"]
                }
            )
        new_process["stage_ids"] = new_stage_ids
        trees = await get_trees(self.__database, new_process["tree_ids"])

        response_data = {
            "process_id": str(process.inserted_id),
            "name": create_process_data["name"],
            "stages": new_stages,
            "trees": trees,
        }
        return success({
            "process": response_data
        })

    async def update_process(self, process_id, update_process):
        update_process["tree_ids"] = [
            ObjectId(tree_id) for tree_id in update_process["tree_ids"]]
        update_process_data = {
            "name": update_process["name"],
            "tree_ids": update_process["tree_ids"],
        }

        updated_process = await self.__database.conn.process.find_one_and_update(
            {"_id": ObjectId(process_id)},
            {"$set": update_process_data},
            return_document=True
        )

        if not updated_process:
            return ApiNotFound("Process not found")
        
        stage_ids = []
        for stage in update_process.get("stages") or []:
            if stage.get("stage_id") is not None:
                stage_ids.append(ObjectId(stage["stage_id"]))
        # delete stages of process that not in stage_ids
        await self.__database.conn.stage.delete_many({"process_id": ObjectId(process_id), "_id": {"$nin": stage_ids}})
        for idx, stage in enumerate(update_process["stages"]):
            stage["idx"] = idx
            stage["process_id"] = ObjectId(process_id)
            stage = await update_stage(self.__database, stage)
            # stage.pop("_id")
            # stage_ids.append(ObjectId(new_stage["stage_id"]))
            # stages.append(
            #     {
            #         "stage_id": new_stage["stage_id"],
            #         "process_id": str(new_stage["process_id"]),
            #         "name": new_stage["name"],
            #         "steps": new_stage["steps"]
            #     }
            # )

        # update season's process
        if updated_process.get("season_id"):
            completed = check_season_completed(update_process["stages"])
            #TODO: save data to blockchain
            # if completed:
            #     await save_season_to_blockchain(self.__database, self.__sdk_handler, updated_process["season_id"])
        stages = await get_process_stages(self.__database, updated_process["_id"])
        updated_process["process_id"] = str(updated_process["_id"])
        del updated_process["_id"]
        updated_process["stages"] = stages

        updated_process["tree_ids"] = [
            str(tree_id) for tree_id in updated_process["tree_ids"]]
        if updated_process.get("season_id"):
            updated_process["season_id"] = str(updated_process["season_id"])

        if updated_process.get("template_process_id"):
            updated_process["template_process_id"] = str(updated_process["template_process_id"])
        return success({
            "updated_process": updated_process
        })

    async def delete_process(self, process_id):
        deleted_process = await self.__database.conn.process.find_one_and_delete(
            {"_id": ObjectId(process_id)}
        )
        if not deleted_process:
            return ApiNotFound("Process not found")
        return success({
            "process_id": str(deleted_process["_id"])
        })

    async def get_steps(self, process_id):
        process = await self.__database.conn.process.find_one({"_id": ObjectId(process_id)}, {"stages": 1})
        if not process:
            return ApiNotFound("Process not found")
        steps = []
        for stage in process["stages"]:
            steps = steps + stage["steps"]
        return success({
            "steps": steps
        })

    async def get_process_of_tree():
        pass
