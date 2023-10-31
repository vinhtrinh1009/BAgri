
import sys
import logging
import asyncio
from settings import config
from config.logging_config import get_logger
from database import Database
from includes.broker_client import BrokerClient
from dapp.event_handler import DappHandler

LOGGER = logging.getLogger(__name__)

class EtherDriver:
    def __init__(self, driver_config):
        self.database = Database(host=driver_config["database"]["host"],
                                 port=driver_config["database"]["port"],
                                 username=driver_config["database"]["username"],
                                 password=driver_config["database"]["password"],
                                 dbname=driver_config["database"]["db_name"])

        self.broker_client = BrokerClient(username=driver_config["rabbitmq"]["username"],
                                          password=driver_config["rabbitmq"]["password"],
                                          host=driver_config["rabbitmq"]["host"],
                                          port=driver_config["rabbitmq"]["port"])
        self.dapp_handler = DappHandler(database=self.database,
                                        broker_client=self.broker_client)

    async def setup_service(self, loop):
        await self.database.connect()

        event_handlers = {
            "driver.ethereum.request.create_dapp": self.dapp_handler.handle_create_dapp,
            "driver.ethereum.request.update_dapp": self.dapp_handler.handle_update_dapp,
            "driver.ethereum.request.delete_dapp": self.dapp_handler.handle_delete_dapp,
        }
        loop.create_task(self.broker_client.consume("ethereum.coreservice.events",
                                                    event_handlers))

    async def close_connection(self):
        await self.broker_client.close()

driver = EtherDriver(config)
loop = asyncio.get_event_loop()
loop.run_until_complete(driver.setup_service(loop))
try:
    loop.run_forever()
finally:
    loop.run_until_complete(driver.close_connection())
    _LOGGER.debug("ERROR")

loop.close()



# app = web.Application()
# handler = Handler('Applications')
# app['secret_key'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

# app.router.add_route("POST", "/v1/business", handler.generate_business)

# cors = aiohttp_cors.setup(
#     app,
#     defaults={
#         "*": aiohttp_cors.ResourceOptions(
#             allow_credentials=True, expose_headers="*", allow_headers="*",
#         )
#     },
# )

# for route in list(app.router.routes()):
#     cors.add(route)

# web.run_app(app, host='0.0.0.0', port=8089)