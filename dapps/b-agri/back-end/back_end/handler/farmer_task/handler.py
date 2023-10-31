from utils.response import success, ApiBadRequest, ApiInternalError
from utils.logging import get_logger

_LOGGER = get_logger(__name__)

class FarmerTaskHandler:
    def __init__(self, database):
        self.__database = database

    async def get_farmer_tasks(self):
        return success({
            "farmer_tasks": [{
                "farmer_task_id": "61971de8d305bde3e0598b69",
                "farmer_id": "61971de8d305bde3e0598c89",
                "task_id": "61971de8d305bde3e0598d69",
                "status": "Doing"
            },
            {
                "farmer_task_id": "61971de8d305bde3e0598b69",
                "farmer_id": "61971de8d305bde3e0598c89",
                "task_id": "61971de8d305bde3e0598d69",
                "status": "Done"
            },
            {
                "farmer_task_id": "61971de8d305bde3e0598b69",
                "farmer_id": "61971de8d305bde3e0598c89",
                "task_id": "61971de8d305bde3e0598d69",
                "status": "Todo"
            }]
        }) 

    async def get_farmer_task(self, farmer_task_id):
        return success({
            "farmer_task_task": {
                "farmer_task_id": farmer_task_id,
                "farmer_id": "61971de8d305bde3e0598c89",
                "task_id": "61971de8d305bde3e0598d69",
                "status": "Todo"
            }
        })

    async def create_farmer_task(self, new_farmer_task):
        return success({
            "farmer_task_id": "61971de8d305bde3e0598b68"
        })

    async def update_farmer_task(self, farmer_task_id, update_farmer_task):
        return success({
            "updated_farmer_task": {
                "farmer_task_id": farmer_task_id,
                "farmer_id": "61971de8d305bde3e0598c89",
                "task_id": "61971de8d305bde3e0598d69",
                "status": "Doing"
            }
        })

    async def delete_farmer_task(self, farmer_task_id):
        return success({
            "farmer_task_id": farmer_task_id
        })
        