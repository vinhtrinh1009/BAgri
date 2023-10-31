from utils.response import success, ApiBadRequest, ApiInternalError
from utils.logging import get_logger

_LOGGER = get_logger(__name__)

class WorkdayHandler:
    def __init__(self, database):
        self.__database = database

    async def get_workdays(self):
        return success({
            "workdays": [{
                "workday_id": "61971de8d305bde3e0598b69",
                "farmer_id": "61971de8d305bde3e1598b69",
                "total": 10,
                "month": 1
            },
            {
                "workday_id": "61971de8d305bde3e0598234",
                "farmer_id": "61971de8d305bde3e1598b69",
                "total": 10,
                "month": 2
            },
            {
                "workday_id": "61971de8d305bde3e0598231",
                "farmer_id": "61971de8d305bde3e1598b69",
                "total": 10,
                "month": 1
            }]
        }) 

    async def get_workday(self, workday_id):
        return success({
            "workday": {
                "workday_id": workday_id,
                "farmer_id": "61971de8d305bde3e1598b69",
                "total": 10,
                "month": 1
            }
        })

    async def create_workday(self, new_workday):
        return success({
            "workday_id": "61971de8d305bde3e0598b68"
        })

    async def update_workday(self, workday_id, update_workday):
        return success({
            "updated_workday": {
                "workday_id": workday_id,
                "farmer_id": "61971de8d305bde3e1598b69",
                "total": 10,
                "month": 2
            }
        })

    async def delete_workday(self, workday_id):
        return success({
            "workday_id": workday_id
        })