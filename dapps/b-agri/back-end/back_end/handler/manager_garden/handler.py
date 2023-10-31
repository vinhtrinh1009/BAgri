from utils.response import success, ApiBadRequest, ApiInternalError
from utils.logging import get_logger

_LOGGER = get_logger(__name__)

class ManagerGardenHandler:
    def __init__(self, database):
        self.__database = database

    async def get_manager_gardens(self):
        return success({
            "manager_gardens": [{
                "manager_garden_id": "61971de8d305bde3e0598c79",
                "manager_id": "61971de8d305bde3e0598b79",
                "garden_id": "61971de8d305bde3e0598b69"
            },
            {
                "manager_garden_id": "61971de8d305bde3e0598c79",
                "manager_id": "61971de8d305bde3e0598b7a",
                "garden_id": "61971de8d305bde3e0598b6a"
            },
            {
                "manager_garden_id": "61971de8d305bde3e0598c79",
                "manager_id": "61971de8d305bde3e0598b7b",
                "garden_id": "61971de8d305bde3e0598b6b"
            }]
        }) 

    async def get_manager_garden(self, manager_garden_id):
        return success({
            "manager_garden": {
                "manager_garden_id": manager_garden_id,
                "manager_id": "61971de8d305bde3e0598b79",
                "garden_id": "61971de8d305bde3e0598b69"
            }
        })

    async def create_manager_garden(self, new_manager_garden):
        return success({
            "manager_garden_id": "61971de8d305bde3e0598b80"
        })

    async def update_manager_garden(self, manager_garden_id, update_manager_garden):
        return success({
            "updated_manager_garden": {
                "manager_garden_id": manager_garden_id,
                "manager_id": "61971de8d305bde3e0598b69",
                "garden_id": "61971de8d305bde3e0598b69"
            }
        })

    async def delete_manager_garden(self, manager_garden_id):
        return success({
            "manager_garden_id": manager_garden_id
        })