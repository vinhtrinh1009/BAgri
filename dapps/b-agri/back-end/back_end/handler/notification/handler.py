from unittest import result
from utils.response import success, ApiBadRequest, ApiInternalError, ApiNotFound
from utils.logging import get_logger

from bson.objectid import ObjectId
from datetime import datetime

_LOGGER = get_logger(__name__)

class NotificationHandler:
    def __init__(self, database):
        self.__database = database

    async def get_notifications(self, user_id):
        filter_obj = {}
        filter_obj["user_id"] = user_id
        notifications = await self.__database.conn.notification.find(filter_obj, {"user_id":0}).to_list(length=None)
        if notifications:
            for notification in notifications:
                notification['notification_id'] = str(notification['_id'])
                dt_object = datetime.fromtimestamp(notification["created_at"])
                notification["created_at"] = str(dt_object)
                del notification['_id']
        result = notifications[::-1]
        return success({
            "notifications": result
        }) 

    async def get_notification(self, notification_id):
        notification = await self.__database.conn.notification.find_one({"_id": ObjectId(notification_id)}, {"user_id":0, "seen":0})
        if not notification:
            return ApiNotFound("Notification not found")
        
        dt_object = datetime.fromtimestamp(notification["created_at"])
        notification["created_at"] = str(dt_object)
        del notification['_id']

        modification = {
            "seen": True
        }

        await self.__database.conn.notification.find_one_and_update(
            {"_id": ObjectId(notification_id)},
            {"$set": modification},
            return_document=True
        )

        return success({
            "notification": notification
        })

    async def create_notification(self, new_notification):
        return success({
            "notification_id": "61971de8d305bde3e0598b80"
        })

    async def update_notification(self, notification_id, update_notification):
        return success({
            "updated_notification": {
                "notification_id": notification_id,
                "title": "Thong bao cong viec ngay 11/01/2022",
                "description": "Hoan thanh tot"
            }
        })

    async def delete_notification(self, notification_id):
        return success({
            "notification_id": notification_id
        })
