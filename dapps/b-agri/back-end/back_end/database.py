import asyncio

import motor.motor_asyncio as aiomotor
from pymongo.errors import ServerSelectionTimeoutError
from utils.logging import get_logger

_LOGGER = get_logger(__name__)

class Database:
    def __init__(self, mongodb_url,  dbname):
        self._mongo_uri = mongodb_url
        self._dbname = dbname
        self.conn = None
    
    async def connect(self, retries=2, delay=1):
        _LOGGER.info(f"Connecting to database on {self._mongo_uri}")

        for attempt in range(retries):
            try:
                self.conn = aiomotor.AsyncIOMotorClient(self._mongo_uri)[self._dbname]
                _LOGGER.info(f"List collection: {await self.conn.list_collection_names()}")
                _LOGGER.info("Successfully connected to the database")
                return
            except ServerSelectionTimeoutError:
                if attempt == retries-1:
                    _LOGGER.error("Cannot connect to the database")
                    raise ServerSelectionTimeoutError
                else:
                    _LOGGER.debug("Database connection failed")
                    await asyncio.sleep(delay)

    async def create_indexes(self):
        user_col = self.conn.user
        await user_col.create_index("username", unique=True)
