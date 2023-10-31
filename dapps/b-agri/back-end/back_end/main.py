import os
import sys

import jinja2
import aiohttp_jinja2
import aiohttp_cors
from aiohttp import web
from database import Database
from routes_handler import RouteHandler
from settings import config
from utils.logging import get_logger
from utils.middleware import self_authorize
from sdk.py_handler import Handler as SdkHandler

_LOGGER = get_logger(__name__)

app = web.Application(middlewares=[self_authorize])
app['config'] = config
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)


async def setup_service(app):
    try:
        app["database"] = Database(
            mongodb_url=app["config"]["mongodb"]["url"],
            dbname=app["config"]["mongodb"]["db_name"])

        app["sdk_handler"] = SdkHandler("0x02F0eAFD8B99C11c894059F24010Ec08479A79fD", "da87a5aeb606edb43c31fb8ec02d61b69d024590b5368b77c50c8d52ae603cdf")
        await app["database"].connect()
        await app["database"].create_indexes()

        handler = RouteHandler(app["database"], app["sdk_handler"])

        # Farmer
        app.router.add_route("GET", "/v1/farmers", handler.get_farmers)
        app.router.add_route(
            "GET",
            "/v1/farmers/{farmer_id}",
            handler.get_farmer)
        app.router.add_route("POST", "/v1/farmers", handler.create_farmer)
        app.router.add_route(
            "PUT",
            "/v1/farmers/{farmer_id}",
            handler.update_farmer)
        app.router.add_route(
            "DELETE",
            "/v1/farmers/{farmer_id}",
            handler.delete_farmer)

        # Farmer task
        app.router.add_route(
            "GET",
            "/v1/farmer-tasks",
            handler.get_farmer_tasks)
        app.router.add_route(
            "GET",
            "/v1/farmer-tasks/{farmer_task_id}",
            handler.get_farmer_task)
        app.router.add_route(
            "POST",
            "/v1/farmer-tasks",
            handler.create_farmer_task)
        app.router.add_route(
            "PUT",
            "/v1/farmer-tasks/{farmer_task_id}",
            handler.update_farmer_task)
        app.router.add_route(
            "DELETE",
            "/v1/farmer-tasks/{farmer_task_id}",
            handler.delete_farmer_task)

        # Garden
        app.router.add_route("GET", "/v1/gardens", handler.get_gardens)
        app.router.add_route(
            "GET",
            "/v1/gardens/{garden_id}",
            handler.get_garden)
        app.router.add_route("POST", "/v1/gardens", handler.create_garden)
        app.router.add_route(
            "PUT",
            "/v1/gardens/{garden_id}",
            handler.update_garden)
        app.router.add_route(
            "DELETE",
            "/v1/gardens/{garden_id}",
            handler.delete_garden)

        # Manager garden
        app.router.add_route(
            "GET",
            "/v1/manager-gardens",
            handler.get_manager_gardens)
        app.router.add_route(
            "GET",
            "/v1/manager-gardens/{manager_garden_id}",
            handler.get_manager_garden)
        app.router.add_route(
            "POST",
            "/v1/manager-gardens",
            handler.create_manager_garden)
        app.router.add_route(
            "PUT",
            "/v1/manager-gardens/{manager_garden_id}",
            handler.update_manager_garden)
        app.router.add_route(
            "DELETE",
            "/v1/manager-gardens/{manager_garden_id}",
            handler.delete_manager_garden)

        # Notification
        app.router.add_route(
            "GET",
            "/v1/notifications",
            handler.get_notifications)
        app.router.add_route(
            "GET",
            "/v1/notifications/{notification_id}",
            handler.get_notification)
        app.router.add_route(
            "POST",
            "/v1/notifications",
            handler.create_notification)
        app.router.add_route(
            "PUT",
            "/v1/notifications/{notification_id}",
            handler.update_notification)
        app.router.add_route(
            "DELETE",
            "/v1/notifications/{notification_id}",
            handler.delete_notification)

        # Process
        app.router.add_route("GET", "/v1/processes", handler.get_processes)
        app.router.add_route(
            "GET",
            "/v1/processes_by_tree",
            handler.get_processes_by_tree)
        app.router.add_route(
            "GET",
            "/v1/processes/{process_id}",
            handler.get_process)
        app.router.add_route("POST", "/v1/processes", handler.create_process)
        app.router.add_route(
            "PUT",
            "/v1/processes/{process_id}",
            handler.update_process)
        app.router.add_route(
            "DELETE",
            "/v1/processes/{process_id}",
            handler.delete_process)
        app.router.add_route(
            "GET",
            "/v1/processes/{process_id}/steps",
            handler.get_process_steps)

        # Stage
        app.router.add_route("GET", "/v1/stages", handler.get_stages)
        app.router.add_route("GET", "/v1/stages/{stage_id}", handler.get_stage)
        app.router.add_route("POST", "/v1/stages", handler.create_stage)
        app.router.add_route(
            "PUT",
            "/v1/stages/{stage_id}",
            handler.update_stage)
        app.router.add_route(
            "DELETE",
            "/v1/stages/{stage_id}",
            handler.delete_stage)

        # Season
        app.router.add_route("GET", "/v1/seasons", handler.get_seasons)
        app.router.add_route(
            "GET",
            "/v1/seasons/{season_id}",
            handler.get_season)
        app.router.add_route(
            "GET",
            "/v1/seasons/{season_id}/process",
            handler.get_season_process)
        app.router.add_route(
            "PUT",
            "/v1/seasons/{season_id}/process",
            handler.update_season_process)
        app.router.add_route(
            "GET",
            "/v1/seasons/{season_id}/steps",
            handler.get_season_steps)
        app.router.add_route(
            "GET",
            "/v1/seasons/network/{season_id}",
            handler.get_season_from_network)
        app.router.add_route(
            "POST",
            "/v1/seasons/{season_id}/qr_code",
            handler.create_season_qr_code)
        app.router.add_route(
            "GET",
            "/v1/seasons/{season_id}/current_step",
            handler.get_current_season_step)
        app.router.add_route("POST", "/v1/seasons", handler.create_season)
        app.router.add_route(
            "PUT",
            "/v1/seasons/{season_id}",
            handler.update_season)
        app.router.add_route(
            "DELETE",
            "/v1/seasons/{season_id}",
            handler.delete_season)
        app.router.add_route(
            "GET",
            "/v1/seasons/{season_id}/process_steps",
            handler.get_season_process_steps)

        # Task
        app.router.add_route("GET", "/v1/tasks", handler.get_tasks)
        app.router.add_route("GET", "/v1/tasks/{task_id}", handler.get_task)
        app.router.add_route("POST", "/v1/tasks", handler.create_task)
        app.router.add_route("PUT", "/v1/tasks/{task_id}", handler.update_task)
        app.router.add_route(
            "DELETE",
            "/v1/tasks/{task_id}",
            handler.delete_task)

        # Tree
        app.router.add_route("GET", "/v1/trees", handler.get_trees)
        app.router.add_route("GET", "/v1/trees/{tree_id}", handler.get_tree)
        app.router.add_route("POST", "/v1/trees", handler.create_tree)
        app.router.add_route("PUT", "/v1/trees/{tree_id}", handler.update_tree)
        app.router.add_route(
            "DELETE",
            "/v1/trees/{tree_id}",
            handler.delete_tree)

        # auth
        app.router.add_route("POST", "/v1/login", handler.login)
        app.router.add_route("POST", "/v1/registry", handler.create_user)
        app.router.add_route("GET", "/v1/me", handler.me)
        app.router.add_route("POST", "/v1/reset-password", handler.reset_password)
        app.router.add_route("PUT", "/v1/change-password", handler.change_password)

        # user
        app.router.add_route("GET", "/v1/users", handler.get_users)
        app.router.add_route("GET", "/v1/users/{user_id}", handler.get_user)
        app.router.add_route("PUT", "/v1/users/{user_id}", handler.update_user)
        app.router.add_route(
            "DELETE",
            "/v1/users/{user_id}",
            handler.delete_user)
        app.router.add_route("GET", "/v1/managers", handler.get_managers)

        # User notification
        app.router.add_route(
            "GET",
            "/v1/user-notifications",
            handler.get_user_notifications)
        app.router.add_route(
            "GET",
            "/v1/user-notifications/{user_notification_id}",
            handler.get_user_notification)
        app.router.add_route(
            "POST",
            "/v1/user-notifications",
            handler.create_user_notification)
        app.router.add_route(
            "PUT",
            "/v1/user-notifications/{user_notification_id}",
            handler.update_user_notification)
        app.router.add_route(
            "DELETE",
            "/v1/user-notifications/{user_notification_id}",
            handler.delete_user_notification)

        # Workday
        app.router.add_route("GET", "/v1/workdays", handler.get_workdays)
        app.router.add_route(
            "GET",
            "/v1/workdays/{workday_id}",
            handler.get_workday)
        app.router.add_route("POST", "/v1/workdays", handler.create_workday)
        app.router.add_route(
            "PUT",
            "/v1/workdays/{workday_id}",
            handler.update_workday)
        app.router.add_route(
            "DELETE",
            "/v1/workdays/{workday_id}",
            handler.delete_workday)

        # file handler
        app.router.add_route("POST", "/v1/files", handler.upload_file)
        app.add_routes([web.static('/static', './static')])

        app.router.add_route(
            "GET",
            "/v1/steps",
            handler.get_steps)
        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )},
        )

        for route in list(app.router.routes()):
            cors.add(route)

    except Exception as err:
        _LOGGER.debug(err)
        sys.exit(1)

app.on_startup.append(setup_service)
web.run_app(app)
