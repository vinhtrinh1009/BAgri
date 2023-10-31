from utils.response import success, ApiBadRequest, ApiInternalError
from utils.logging import get_logger

_LOGGER = get_logger(__name__)

class StageHandler:
    def __init__(self, database):
        self.__database = database

    async def get_stages(self):
        return success({
            "stages": [{
                "stage_id": "61971de8d305bde3e0598b79",
                "process_id": "61971de8d305bde3e0598b80",
                "steps": [],
                "duration": 1
            },
            {
                "stage_id": "61971de8d305bde3e0598bd12",
                "process_id": "61971de8d305bde3e0598b80",
                "steps": [],
                "duration": 2
            }]
        }) 

    async def get_stage(self, stage_id):
        return success({
            "stage": {
                "stage_id": stage_id,
                "process_id": "61971de8d305bde3e0598b80",
                "steps": [],
                "duration": 2
            }
        })

    async def create_stage(self, new_stage):
        return success({
            "stage_id": "61971de8d305bde3e0598b81"
        })

    async def update_stage(self, stage_id, update_stage):
        return success({
            "updated_stage": {
                "stage_id": stage_id,
                "process_id": "61971de8d305bde3e0598b80",
                "steps": [],
                "duration": 5
            }
        })

    async def delete_stage(self, stage_id):
        return success({
            "stage_id": stage_id
        })