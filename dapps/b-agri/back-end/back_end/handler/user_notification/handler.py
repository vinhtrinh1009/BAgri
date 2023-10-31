from utils.response import success, ApiBadRequest, ApiInternalError
from utils.logging import get_logger

_LOGGER = get_logger(__name__)

class UserNotificationHandler:
    def __init__(self, database):
        self.__database = database

    async def get_user_notifications(self):
        return success({
            "user_notifications": [{
                "user_notification_id": "61971de8d305bde3e0598b79",
                "user_id": "61971de8d305bde3e0598b79",
                "notification_id": "61971de8d305bde3e0598b79",
                "seen": False
            },
            {
                "user_notification_id": "61971de8d305bde3e0598b80",
                "user_id": "61971de8d305bde3e0598b79",
                "notification_id": "61971de8d305bde3e0598b81",
                "seen": True
            }]
        }) 

    async def get_user_notification(self, user_notification_id):
        return success({
            "user_notification": {
                "user_notification_id": user_notification_id,
                "user_id": "61971de8d305bde3e0598b79",
                "notification_id": "61971de8d305bde3e0598b79",
                "seen": False
            }
        })

    async def create_user_notification(self, new_user_notification):
        return success({
            "user_notification_id": "61971de8d305bde3e0598b80"
        })

    async def update_user_notification(self, user_notification_id, update_user_notification):
        return success({
            "updated_user_notification": {
                "user_notification_id": user_notification_id,
                "user_id": "61971de8d305bde3e0598b79",
                "notification_id": "61971de8d305bde3e0598b79",
                "seen": True
            }
        })

    async def delete_user_notification(self, user_notification_id):
        return success({
            "user_notification_id": user_notification_id
        })