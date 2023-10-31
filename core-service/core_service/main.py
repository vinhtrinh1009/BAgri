import sys

from aiohttp import web, ClientSession
import aiohttp_cors
import asyncio

from settings import config
from utils.logging import get_logger
from database import Database
from routes_handler import RouteHandler
from utils.broker_client import BrokerClient
from utils.middleware import self_authorize
from network.event_handler import handle_create_network_event, handle_update_network_event, handle_delete_network_event, handle_create_resource_event
from dapp.event_handler import handle_create_dapp_event, handle_update_dapp_event, handle_rollback_update_dapp_event, handle_delete_dapp_event

_LOGGER = get_logger(__name__)

app = web.Application(middlewares=[self_authorize], client_max_size=1024 ** 2)

async def setup_service(app):
    try:
        app["database"] = Database(host=config["database"]["host"],
                                   port=config["database"]["port"],
                                   username=config["database"]["username"],
                                   password=config["database"]["password"],
                                   dbname=config["database"]["db_name"])
        await app["database"].connect()

        app["broker_client"] = BrokerClient(username=config["rabbitmq"]["username"],
                                            password=config["rabbitmq"]["password"],
                                            host=config["rabbitmq"]["host"],
                                            port=config["rabbitmq"]["port"])
        event_handlers = {
            "coreservice.events.create_network": handle_create_network_event,
            "coreservice.events.update_network": handle_update_network_event,
            "coreservice.events.delete_network": handle_delete_network_event,
            "coreservice.events.create_resource": handle_create_resource_event,
            "coreservice.events.create_dapp": handle_create_dapp_event,
            "coreservice.events.update_dapp": handle_update_dapp_event,
            "coreservice.events.rollback_update_dapp": handle_rollback_update_dapp_event,
            "coreservice.events.delete_dapp": handle_delete_dapp_event,
        }
        asyncio.create_task(app["broker_client"].consume("coreservice.events",
                                                         event_handlers,
                                                         app["database"]))

        handler = RouteHandler(app["database"], app["broker_client"])

        app.router.add_route("GET", "/v1/healthz", handler.healthz)

        app.router.add_route("POST", "/v1/networks", handler.create_network)
        app.router.add_route("POST", "/v1/networks/{network_id}/retry", handler.retry_create_network)

        app.router.add_route("PUT", "/v1/networks/{network_id}", handler.update_network)
        app.router.add_route("PUT", "/v1/networks/{network_id}/retry", handler.retry_update_network)
        app.router.add_route("PUT", "/v1/networks/{network_id}/rollback", handler.rollback_update_network)

        app.router.add_route("GET", "/v1/networks", handler.get_user_networks)
        app.router.add_route("GET", "/v1/networks/{network_id}", handler.get_network)

        app.router.add_route("DELETE", "/v1/networks/{network_id}", handler.delete_network)
        # app.router.add_route("DELETE", "/v1/networks/{network_id}/retry", handler.retry_delete_network)

        app.router.add_route("POST", "/v1/networks/{network_id}/resources", handler.create_resource)
        app.router.add_route("GET", "/v1/networks/{network_id}/resources", handler.get_network_resources)
        #
        app.router.add_route("POST", "/v1/dapps", handler.create_dapp)
        app.router.add_route("POST", "/v1/dapps/{dapp_id}/retry", handler.retry_create_dapp)

        app.router.add_route("PUT", "/v1/dapps/{dapp_id}", handler.update_dapp)
        app.router.add_route("PUT", "/v1/dapps/{dapp_id}/retry", handler.retry_update_dapp)
        app.router.add_route("PUT", "/v1/dapps/{dapp_id}/rollback", handler.rollback_update_dapp)

        app.router.add_route("GET", "/v1/dapps", handler.get_user_dapps)
        app.router.add_route("GET", "/v1/dapps/{dapp_id}", handler.get_dapp)
        
        app.router.add_route("DELETE", "/v1/dapps/{dapp_id}", handler.delete_dapp)
        app.router.add_route("DELETE", "/v1/dapps/{dapp_id}/retry", handler.retry_delete_dapp)
        
        app.router.add_route("GET", "/v1/sdks/{sdk_key}", handler.get_dapp_by_sdk_key)

        

        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                    allow_methods="*"
                )
            },
        )
        for route in list(app.router.routes()):
            cors.add(route)

    except Exception as err:
        print(err)
        sys.exit(1)


async def cleanup_resources(app):
    await app["broker_client"].close()


app.on_startup.append(setup_service)
app.on_cleanup.append(cleanup_resources)

web.run_app(app)
