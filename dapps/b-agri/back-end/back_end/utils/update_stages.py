from bson.objectid import ObjectId
import pymongo


async def update_step(db, step):
    """
    the step includes the _id, remember to pop it
    """
    if step.get("step_id") is not None:
        step_id = step["step_id"]
        step.pop("step_id")
        await db.conn.step.find_one_and_update(
            {"_id": ObjectId(step_id)},
            {"$set": step}
        )
        step["step_id"] = step_id
    else:
        await db.conn.step.insert_one(step)
        step["step_id"] = str(step["_id"])
    step["stage_id"] = str(step["stage_id"])
    return step


async def update_stage(db, stage):
    """
    if stage.get("stage_id") is not, create new
    otherwise, update it
    """
    stage_id = stage.get("stage_id")
    if stage_id is not None:
        step_ids = []
        for step in stage.get("steps") or []:
            if step.get("step_id") is not None:
                step_ids.append(ObjectId(step["step_id"]))
        # delete steps of stage that not in step_ids
        await db.conn.step.delete_many({"stage_id": ObjectId(stage_id), "_id": {"$nin": step_ids}})

        steps = []

        for idx, step in enumerate(stage.get("steps") or []):
            step["idx"] = idx
            step["stage_id"] = ObjectId(stage_id)
            processed_step = await update_step(db, step)

        await db.conn.step.find_one_and_update(
            {"_id": ObjectId(stage_id)},
            {"$set": {
                "name": stage["name"],
                "idx": stage["idx"]
            }
            }
        )
        stage["steps"] = steps
    else:
        step_ids = []
        steps = []
        new_stage = {
            "name": stage["name"],
            "process_id": stage["process_id"],
            "idx": stage["idx"],
        }
        await db.conn.stage.insert_one(
            new_stage
        )
        for idx, step in enumerate(stage.get("steps") or []):
            step["idx"] = idx
            step["stage_id"] = new_stage["_id"]
            processed_step = await update_step(db, step)
            step_ids.append(ObjectId(processed_step["step_id"]))
            processed_step.pop("_id")
            steps.append(processed_step)

        stage = new_stage
        stage["stage_id"] = str(new_stage["_id"])
        stage["steps"] = steps
    return stage

    # for stage in process["stages"]:
    #     for step in stage["steps"]:
    #         if step.get("step_id") is not None:
    #             step_id=step["step_id"]
    #             step.pop("step_id")
    #             await self.__database.conn.step.find_one_and_update(
    #                 {"_id": ObjectId(step_id)},
    #                 {"$set": step}
    #             )
    #             step["step_id"]=step_id
    #         else:
    #             await self.__database.conn.step.insert_one(step)
    #             step["step_id"]=str(step["_id"])
    #             step.pop("_id")
    #     updated_stages.append(
    #         {"steps": [ObjectId(step["step_id"]) for step in stage["steps"]]})


async def get_trees(db, tree_ids):
    trees = await db.conn.tree.find(
        {"_id": {"$in": tree_ids}}, {"_id": 1, "name": 1}
    ).to_list(length=None)

    return [{
        "tree_id": str(tree["_id"]),
        "name": tree["name"]
    } for tree in trees]


async def get_stage(db, stage_id: ObjectId):
    stage_doc = await db.conn.stage.find_one({"_id": ObjectId(stage_id)})
    stage = {}
    stage["stage_id"] = str(stage_doc["_id"])
    stage["name"] = stage_doc["name"]
    stage["steps"] = []
    step_docs = await db.conn.step.find({"stage_id": stage_doc["_id"]}).sort([("idx", pymongo.ASCENDING)]).to_list(None)
    for step_doc in step_docs:
        step_doc["step_id"] = str(step_doc["_id"])
        step_doc.pop("_id")
        stage["steps"].append({
            "step_id": str(step_doc["_id"]),
            "name": step_doc["name"],
            "from_day": step_doc["from_day"],
            "to_day": step_doc["to_day"],
        })
    return stage


async def get_process_stages(db, process_id):
    stage_docs = await db.conn.stage.find({"process_id": ObjectId(process_id)}).sort([("idx", pymongo.ASCENDING)]).to_list(None)
    stages = []
    for stage_doc in stage_docs:
        stage = {}
        stage["stage_id"] = str(stage_doc["_id"])
        stage["name"] = stage_doc["name"]
        stage["steps"] = []
        step_docs = await db.conn.step.find({"stage_id": stage_doc["_id"]}).sort([("idx", pymongo.ASCENDING)]).to_list(length=None)
        for step_doc in step_docs:
            step_doc["step_id"] = str(step_doc["_id"])
            step_doc.pop("_id")
            stage["steps"].append({
                "step_id": step_doc["step_id"],
                "idx": step_doc.get("idx"),
                "name": step_doc["name"],
                "from_day": step_doc["from_day"],
                "stage_id": str(step_doc["stage_id"]),
                "to_day": step_doc["to_day"],
                "actual_day": step_doc.get("actual_day")
            })
        stages.append(stage)
    return stages
