import sys
from aiohttp import web, ClientSession
import aiohttp_cors
from settings import config
from routes_handler import RouteHandler
from database import Database
from utils.logging import get_logger
from utils.middleware import authorized
import asyncio

_LOGGER = get_logger(__name__)

app = web.Application(middlewares=[authorized])
app['config'] = config

async def setup_service(app):
    try:
        app["database"] = Database(host=app["config"]["database"]["host"],
                                   port=app["config"]["database"]["port"],
                                   username=app["config"]["database"]["username"],
                                   password=app["config"]["database"]["password"],
                                   dbname=app["config"]["database"]["db_name"])
        await app["database"].connect()

        handler = RouteHandler(app["database"])

        
        app.router.add_route("GET", "/v1/shares", handler.get_shares)
        app.router.add_route("GET", "/v1/shares/{folder_id}", handler.get_child_shares)

        app.router.add_route("GET", "/v1/recents", handler.get_recents)
        app.router.add_route("GET", "/v1/favorites", handler.get_favorites)

        app.router.add_route("GET", "/v1/trashes", handler.get_trashes)
        app.router.add_route("GET", "/v1/trashes/{folder_id}", handler.get_child_trashes)

        app.router.add_route("PUT", "/v1/recovery", handler.recover_all)
        app.router.add_route("DELETE", "/v1/delete", handler.delete_all)
        
        app.router.add_route("GET", "/v1/folders", handler.get_user_folders)
        app.router.add_route("POST", "/v1/folders", handler.create_folder)
        app.router.add_route("GET", "/v1/folders/{folder_id}", handler.get_folder)
        app.router.add_route("GET", "/v1/folders/{folder_id}/download", handler.download_folder)
        app.router.add_route("POST", "/v1/folders/{folder_id}/upload", handler.upload_folder)
        app.router.add_route("PUT", "/v1/folders/{folder_id}/rename", handler.rename_folder)
        app.router.add_route("PUT", "/v1/folders/{folder_id}/move", handler.move_folder)
        app.router.add_route("PUT", "/v1/folders/{folder_id}/copy", handler.copy_folder)
        app.router.add_route("PUT", "/v1/folders/{folder_id}/favorite", handler.favorite_folder)
        app.router.add_route("PUT", "/v1/folders/{folder_id}/unfavorite", handler.unfavorite_folder)
        app.router.add_route("PUT", "/v1/folders/{folder_id}/trash", handler.trash_folder)
        app.router.add_route("PUT", "/v1/folders/{folder_id}/untrash", handler.untrash_folder)
        app.router.add_route("DELETE", "/v1/folders/{folder_id}/delete", handler.delete_folder)

        app.router.add_route("GET", "/v1/files/{file_id}", handler.get_file)
        app.router.add_route("GET", "/v1/files/{file_id}/download", handler.download_file)
        app.router.add_route("POST", "/v1/files/{folder_id}/upload", handler.upload_file)
        app.router.add_route("PUT", "/v1/files/{file_id}/rename", handler.rename_file)
        app.router.add_route("PUT", "/v1/files/{file_id}/move", handler.move_file)
        app.router.add_route("PUT", "/v1/files/{file_id}/copy", handler.copy_file)
        app.router.add_route("PUT", "/v1/files/{file_id}/favorite", handler.favorite_file)
        app.router.add_route("PUT", "/v1/files/{file_id}/unfavorite", handler.unfavorite_file)
        app.router.add_route("PUT", "/v1/files/{file_id}/trash", handler.trash_file)
        app.router.add_route("PUT", "/v1/files/{file_id}/untrash", handler.untrash_file)
        app.router.add_route("DELETE", "/v1/files/{file_id}/delete", handler.delete_file)

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
        _LOGGER.debug(err)
        sys.exit(1)

app.on_startup.append(setup_service)
web.run_app(app)
