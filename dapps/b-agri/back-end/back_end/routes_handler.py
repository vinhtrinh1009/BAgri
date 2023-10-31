import os
from datetime import datetime
from json.decoder import JSONDecodeError
import traceback
from settings import config


from handler.step.handler import StepHandler
from handler.farmer.handler import FarmerHandler
from handler.farmer_task.handler import FarmerTaskHandler
from handler.garden.handler import GardenHandler
from handler.manager_garden.handler import ManagerGardenHandler
from handler.notification.handler import NotificationHandler
from handler.process.handler import ProcessHandler
from handler.season.handler import SeasonHandler
from handler.stage.handler import StageHandler
from handler.task.handler import TaskHandler
from handler.tree.handler import TreeHandler
from handler.user.handler import UserHandler
from handler.user_notification.handler import UserNotificationHandler
from handler.workday.handler import WorkdayHandler
from utils.authorizations import only_manager
from utils.logging import get_logger
from utils.response import ApiBadRequest, ApiInternalError, success

_LOGGER = get_logger(__name__)


class RouteHandler:
    def __init__(self, database, sdk_handler):
        self._garden_handler = GardenHandler(database)
        self._manager_garden_handler = ManagerGardenHandler(database)
        self._notification_handler = NotificationHandler(database)
        self._process_handler = ProcessHandler(database, sdk_handler)
        self._season_handler = SeasonHandler(database, sdk_handler)
        self._stage_handler = StageHandler(database)
        self._task_handler = TaskHandler(database, sdk_handler)
        self._tree_handler = TreeHandler(database, sdk_handler)
        self._user_handler = UserHandler(database)
        self._user_notification_handler = UserNotificationHandler(database)
        self._workday_handler = WorkdayHandler(database)
        self._farmer_handler = FarmerHandler(database)
        self._farmer_task_handler = FarmerTaskHandler(database)
        self._step_handler = StepHandler(database)

    # Farmer
    async def get_farmers(self, request, user_info):
        filter_data = {}
        filter_data["manager_id"] = request.rel_url.query.get("manager_id", "")
        response = await self._farmer_handler.get_farmers(filter_data)
        return response

    async def get_farmer(self, request, user_info):
        farmer_id = request.match_info.get("farmer_id", "")
        _LOGGER.info(f"Get farmer {farmer_id}")
        response = await self._farmer_handler.get_farmer(farmer_id=farmer_id)
        return response

    async def create_farmer(self, request, user_info):
        _LOGGER.info("Create new farmer")
        body = await decode_request(request)
        required_fields = ["manager_id", "fullname", "phone"]
        validate_fields(required_fields, body)
        response = await self._farmer_handler.create_farmer(new_farmer=body)
        return response

    async def update_farmer(self, request, user_info):
        farmer_id = request.match_info.get("farmer_id", "")
        _LOGGER.info(f"Update farmer {farmer_id}")
        body = await decode_request(request)
        response = await self._farmer_handler.update_farmer(farmer_id=farmer_id, update_farmer=body)
        return response

    async def delete_farmer(self, request, user_info):
        farmer_id = request.match_info.get("farmer_id", "")
        _LOGGER.info(f"Delete farmer {farmer_id}")
        response = await self._farmer_handler.delete_farmer(farmer_id=farmer_id)
        return response

    # Farmer task
    async def get_farmer_tasks(self, request, user_info):
        response = await self._farmer_task_handler.get_farmer_tasks()
        return response

    async def get_farmer_task(self, request, user_info):
        farmer_task_id = request.match_info.get("farmer_task_id", "")
        _LOGGER.info(f"Get farmer_task {farmer_task_id}")
        response = await self._farmer_task_handler.get_farmer_task(farmer_task_id=farmer_task_id)
        return response

    async def create_farmer_task(self, request, user_info):
        _LOGGER.info("Create new farmer_task")
        body = await decode_request(request)
        required_fields = ["task_id", "farmer_id", "status"]
        validate_fields(required_fields, body)
        response = await self._farmer_task_handler.create_farmer_task(new_farmer_task=body)
        return response

    async def update_farmer_task(self, request, user_info):
        farmer_task_id = request.match_info.get("farmer_task_id", "")
        _LOGGER.info(f"Update farmer_task {farmer_task_id}")
        body = await decode_request(request)
        response = await self._farmer_task_handler.update_farmer_task(farmer_task_id=farmer_task_id, update_farmer_task=body)
        return response

    async def delete_farmer_task(self, request, _):
        farmer_task_id = request.match_info.get("farmer_task_id", "")
        _LOGGER.info(f"Delete farmer_task {farmer_task_id}")
        response = await self._farmer_task_handler.delete_farmer_task(farmer_task_id=farmer_task_id)
        return response

    # Garden
    @only_manager
    async def get_gardens(self, request, user_info):
        manager_id = request.rel_url.query.get("manager_id", None)
        filter_data = {}
        print(manager_id)
        filter_data["manager_id"] = manager_id
        response = await self._garden_handler.get_gardens(filter_data)
        return response

    @only_manager
    async def get_garden(self, request, user_info):
        garden_id = request.match_info.get("garden_id", "")
        _LOGGER.info(f"Get garden {garden_id}")
        response = await self._garden_handler.get_garden(garden_id=garden_id)
        return response

    @only_manager
    async def create_garden(self, request, user_info):
        _LOGGER.info("Create new garden")
        body = await decode_request(request)
        required_fields = ["name", "area"]
        validate_fields(required_fields, body)
        response = await self._garden_handler.create_garden(new_garden=body)
        return response

    @only_manager
    async def update_garden(self, request, user_info):
        garden_id = request.match_info.get("garden_id", "")
        _LOGGER.info(f"Update garden {garden_id}")
        body = await decode_request(request)
        response = await self._garden_handler.update_garden(garden_id=garden_id, update_garden=body)
        return response

    @only_manager
    async def delete_garden(self, request, user_info):
        garden_id = request.match_info.get("garden_id", "")
        _LOGGER.info(f"Delete garden {garden_id}")
        response = await self._garden_handler.delete_garden(garden_id=garden_id)
        return response

    # Manager
    async def get_manager_gardens(self, request, user_info):
        response = await self._manager_garden_handler.get_manager_gardens()
        return response

    async def get_manager_garden(self, request, user_info):
        manager_garden_id = request.match_info.get("manager_garden_id", "")
        _LOGGER.info(f"Get manager garden {manager_garden_id}")
        response = await self._manager_garden_handler.get_manager_garden(manager_garden_id=manager_garden_id)
        return response

    async def create_manager_garden(self, request, user_info):
        _LOGGER.info("Create new manager garden")
        body = await decode_request(request)
        required_fields = ["manager_id", "garden_id"]
        validate_fields(required_fields, body)
        response = await self._manager_garden_handler.create_manager_garden(new_manager_garden=body)
        return response

    async def update_manager_garden(self, request, user_info):
        manager_garden_id = request.match_info.get("manager_garden_id", "")
        _LOGGER.info(f"Update manager garden {manager_garden_id}")
        body = await decode_request(request)
        response = await self._manager_garden_handler.update_manager_garden(manager_garden_id=manager_garden_id, update_manager_garden=body)
        return response

    async def delete_manager_garden(self, request, user_info):
        manager_garden_id = request.match_info.get("manager_garden_id", "")
        _LOGGER.info(f"Delete manager garden {manager_garden_id}")
        response = await self._manager_garden_handler.delete_manager_garden(manager_garden_id=manager_garden_id)
        return response

    # Notification
    async def get_notifications(self, request, user_info):
        print("Get list notification")
        response = await self._notification_handler.get_notifications(user_info["id"])
        return response

    async def get_notification(self, request, user_info):
        notification_id = request.match_info.get("notification_id", "")
        _LOGGER.info(f"Get notification {notification_id}")
        response = await self._notification_handler.get_notification(notification_id=notification_id)
        return response

    async def create_notification(self, request, user_info):
        _LOGGER.info("Create new notification")
        body = await decode_request(request)
        required_fields = ["title", "description"]
        validate_fields(required_fields, body)
        response = await self._notification_handler.create_notification(new_notification=body)
        return response

    async def update_notification(self, request, user_info):
        notification_id = request.match_info.get("notification_id", "")
        _LOGGER.info(f"Update notification {notification_id}")
        body = await decode_request(request)
        response = await self._notification_handler.update_notification(notification_id=notification_id, update_notification=body)
        return response

    async def delete_notification(self, request, user_info):
        notification_id = request.match_info.get("notification_id", "")
        _LOGGER.info(f"Delete notification {notification_id}")
        response = await self._notification_handler.delete_notification(notification_id=notification_id)
        return response

    # Process
    async def get_processes(self, request, user_info):
        try:
            response = await self._process_handler.get_processes()
            return response
        except Exception as e:
            return ApiInternalError("internal error" + str(e))

    async def get_processes_by_tree(self, request, user_info):
        try:
            tree_id = request.rel_url.query.get("tree_id", "")
            response = await self._process_handler.get_processes_by_tree(tree_id)
            return response
        except Exception as e:
            traceback.print_exc()
            return ApiInternalError("internal error" + str(e))

    async def get_process(self, request, _):
        try:
            process_id = request.match_info.get("process_id", "")
            _LOGGER.info(f"Get process {process_id}")
            response = await self._process_handler.get_process(process_id=process_id)
            return response
        except Exception as e:
            _LOGGER.error(e)
            traceback.print_exc()
            return ApiInternalError("internal error" + str(e))

    async def create_process(self, request, _):
        try:
            _LOGGER.info("Create new process")
            body = await decode_request(request)
            required_fields = ["name"]
            validate_fields(required_fields, body)
            response = await self._process_handler.create_process(new_process=body)
            return response
        except Exception as e:
            traceback.print_exc()
            return ApiInternalError("internal error" + str(e))

    async def update_process(self, request, _):
        try:
            process_id = request.match_info.get("process_id", "")
            _LOGGER.info(f"Update process {process_id}")
            body = await decode_request(request)
            response = await self._process_handler.update_process(process_id=process_id, update_process=body)
            return response
        except Exception as e:
            _LOGGER.error(e)
            traceback.print_exc()
            return ApiInternalError("internal error" + str(e))

    async def delete_process(self, request, _):
        try:
            process_id = request.match_info.get("process_id", "")
            _LOGGER.info(f"Delete process {process_id}")
            response = await self._process_handler.delete_process(process_id=process_id)
            return response
        except Exception as e:
            _LOGGER.error(e)
            traceback.print_exc()
            return ApiInternalError("internal error" + str(e))

    # Season
    async def get_seasons(self, request, user_info):
        response = await self._season_handler.get_seasons()
        return response

    async def get_season(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Get season {season_id}")
        response = await self._season_handler.get_season(season_id=season_id)
        return response

    async def update_season_process(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Get season process {season_id}")
        body = await decode_request(request)
        response = await self._season_handler.update_season_process(season_id=season_id, process=body)
        return response

    async def get_season_steps(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Get season {season_id}")
        response = await self._season_handler.get_season_steps(season_id=season_id)
        return response

    async def get_current_season_step(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Get season {season_id}")
        response = await self._season_handler.get_current_season_step(season_id=season_id)
        return response

    async def get_season_from_network(self, request):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Get season {season_id}")
        response = await self._season_handler.get_season_from_network(request=request, season_id=season_id)
        return response

    async def create_season_qr_code(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Generate qr code {season_id}")
        response = await self._season_handler.generate_qr_code(season_id=season_id)
        return response

    async def get_season_process(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Get season process {season_id}")
        response = await self._season_handler.get_season_process(season_id=season_id)
        return response

    async def create_season(self, request, user_info):
        _LOGGER.info("Create new season")
        body = await decode_request(request)
        required_fields = [
            "name",
            "garden_id",
            "tree_id",
            "process_id",
            "status"]
        validate_fields(required_fields, body)
        response = await self._season_handler.create_season(new_season=body)
        return response

    async def update_season(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Update season {season_id}")
        body = await decode_request(request)
        response = await self._season_handler.update_season(season_id=season_id, update_season=body)
        return response

    async def delete_season(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Delete season {season_id}")
        response = await self._season_handler.delete_season(season_id=season_id)
        return response

    async def get_season_process_steps(self, request, user_info):
        season_id = request.match_info.get("season_id", "")
        _LOGGER.info(f"Get season process steps {season_id}")
        response = await self._season_handler.get_season_process_steps(season_id=season_id)
        return response

    # Stage
    async def get_stages(self, request, user_info):
        response = await self._stage_handler.get_stages()
        return response

    async def get_stage(self, request, user_info):
        stage_id = request.match_info.get("stage_id", "")
        _LOGGER.info(f"Get stage {stage_id}")
        response = await self._stage_handler.get_stage(stage_id=stage_id)
        return response

    async def create_stage(self, request, user_info):
        _LOGGER.info("Create new stage")
        body = await decode_request(request)
        required_fields = ["process_id", "steps", "duration"]
        validate_fields(required_fields, body)
        response = await self._stage_handler.create_stage(new_stage=body)
        return response

    async def update_stage(self, request, user_info):
        stage_id = request.match_info.get("stage_id", "")
        _LOGGER.info(f"Update stage {stage_id}")
        body = await decode_request(request)
        response = await self._stage_handler.update_stage(stage_id=stage_id, update_stage=body)
        return response

    async def delete_stage(self, request, user_info):
        stage_id = request.match_info.get("stage_id", "")
        _LOGGER.info(f"Delete stage {stage_id}")
        response = await self._stage_handler.delete_stage(stage_id=stage_id)
        return response

    # Task
    async def get_tasks(self, request, user_info):
        season_id = request.rel_url.query.get("season_id", "")
        date = request.rel_url.query.get("date", "")
        if season_id and date:
            response = await self._task_handler.get_season_tasks_by_date(season_id=season_id, date=date)
        elif season_id:
            response = await self._task_handler.get_tasks_by_season(season_id=season_id)
        elif date:
            return ApiBadRequest(
                "cannot request season by date, please add season_id")
        else:
            response = await self._task_handler.get_tasks()
        return response

    async def get_task(self, request, user_info):
        task_id = request.match_info.get("task_id", "")
        _LOGGER.info(f"Get task {task_id}")
        response = await self._task_handler.get_task(task_id=task_id)
        return response

    async def create_task(self, request, user_info):
        _LOGGER.info("Create new task")
        body = await decode_request(request)
        required_fields = [
            "manager_id",
            "season_id",
            "name",
            "description",
            "date",
            "start_time",
            "end_time",
            "result"]
        validate_fields(required_fields, body)
        response = await self._task_handler.create_task(new_task=body)
        return response

    async def update_task(self, request, user_info):
        task_id = request.match_info.get("task_id", "")
        _LOGGER.info(f"Update task {task_id}")
        body = await decode_request(request)
        response = await self._task_handler.update_task(task_id=task_id, update_task=body)
        return response

    async def delete_task(self, request, user_info):
        task_id = request.match_info.get("task_id", "")
        _LOGGER.info(f"Delete task {task_id}")
        response = await self._task_handler.delete_task(task_id=task_id)
        return response

    # Tree
    async def get_trees(self, request, user_info):
        response = await self._tree_handler.get_trees()
        return response

    async def get_tree(self, request, user_info):
        tree_id = request.match_info.get("tree_id", "")
        _LOGGER.info(f"Get tree {tree_id}")
        response = await self._tree_handler.get_tree(tree_id=tree_id)
        return response

    async def create_tree(self, request, user_info):
        _LOGGER.info("Create new tree")
        body = await decode_request(request)
        required_fields = ["name"]
        validate_fields(required_fields, body)
        response = await self._tree_handler.create_tree(new_tree=body)
        return response

    async def update_tree(self, request, user_info):
        tree_id = request.match_info.get("tree_id", "")
        _LOGGER.info(f"Update tree {tree_id}")
        body = await decode_request(request)
        response = await self._tree_handler.update_tree(tree_id=tree_id, update_tree=body)
        return response

    async def delete_tree(self, request, user_info):
        tree_id = request.match_info.get("tree_id", "")
        _LOGGER.info(f"Delete tree {tree_id}")
        response = await self._tree_handler.delete_tree(tree_id=tree_id)
        return response

    async def reset_password(self, request):
        body = await decode_request(request)
        required_fields = ["username", "phone"]
        validate_fields(required_fields, body)
        response = await self._user_handler.reset_password(body=body)
        return response

    async def change_password(self, request, user_info):
        body = await decode_request(request)
        required_fields = ["old_password", "new_password", "retype_new_password"]
        validate_fields(required_fields, body)
        response = await self._user_handler.change_password(body=body, user_info=user_info)
        return response

    async def login(self, request):
        body = await decode_request(request)
        required_fields = ["username", "password"]
        validate_fields(required_fields, body)
        response = await self._user_handler.login(body=body)
        return response

    async def me(self, _, user_info):
        return success(user_info)

    async def get_users(self, request, user_info):
        response = await self._user_handler.get_users()
        return response

    async def get_managers(self, request, user_info):
        response = await self._user_handler.get_mangers()
        return response

    async def get_user(self, request, user_info):
        user_id = request.match_info.get("user_id", "")
        _LOGGER.info(f"Get user {user_id}")
        response = await self._user_handler.get_user(user_id=user_id)
        return response

    async def create_user(self, request):
        _LOGGER.info("Create new user")
        body = await decode_request(request)
        required_fields = ["username", "password", "fullname", "role", "phone"]
        validate_fields(required_fields, body)
        response = await self._user_handler.create_user(new_user=body)
        return response

    async def update_user(self, request, user_info):
        user_id = request.match_info.get("user_id", "")
        _LOGGER.info(f"Update user {user_id}")
        body = await decode_request(request)
        response = await self._user_handler.update_user(user_id=user_id, update_user=body)
        return response

    async def delete_user(self, request, user_info):
        user_id = request.match_info.get("user_id", "")
        _LOGGER.info(f"Delete user {user_id}")
        response = await self._user_handler.delete_user(user_id=user_id)
        return response

    # User notification
    async def get_user_notifications(self, request, user_info):
        response = await self._user_notification_handler.get_user_notifications()
        return response

    async def get_user_notification(self, request, user_info):
        user_notification_id = request.match_info.get(
            "user_notification_id", "")
        _LOGGER.info(f"Get user_notification {user_notification_id}")
        response = await self._user_notification_handler.get_user_notification(user_notification_id=user_notification_id)
        return response

    async def create_user_notification(self, request, user_info):
        _LOGGER.info("Create new user_notification")
        body = await decode_request(request)
        required_fields = ["user_id", "notification_id", "seen"]
        validate_fields(required_fields, body)
        response = await self._user_notification_handler.create_user_notification(new_user_notification=body)
        return response

    async def update_user_notification(self, request, user_info):
        user_notification_id = request.match_info.get(
            "user_notification_id", "")
        _LOGGER.info(f"Update user_notification {user_notification_id}")
        body = await decode_request(request)
        response = await self._user_notification_handler.update_user_notification(user_notification_id=user_notification_id, update_user_notification=body)
        return response

    async def delete_user_notification(self, request, user_info):
        user_notification_id = request.match_info.get(
            "user_notification_id", "")
        _LOGGER.info(f"Delete user_notification {user_notification_id}")
        response = await self._user_notification_handler.delete_user_notification(user_notification_id=user_notification_id)
        return response

    # Workday
    async def get_workdays(self, request, user_info):
        response = await self._workday_handler.get_workdays()
        return response

    async def get_workday(self, request, user_info):
        workday_id = request.match_info.get("workday_id", "")
        _LOGGER.info(f"Get workday {workday_id}")
        response = await self._workday_handler.get_workday(workday_id=workday_id)
        return response

    async def create_workday(self, request, user_info):
        _LOGGER.info("Create new workday")
        body = await decode_request(request)
        required_fields = ["farmer_id", "total", "month"]
        validate_fields(required_fields, body)
        response = await self._workday_handler.create_workday(new_workday=body)
        return response

    async def update_workday(self, request, user_info):
        workday_id = request.match_info.get("workday_id", "")
        _LOGGER.info(f"Update workday {workday_id}")
        body = await decode_request(request)
        response = await self._workday_handler.update_workday(workday_id=workday_id, update_workday=body)
        return response

    async def delete_workday(self, request, user_info):
        workday_id = request.match_info.get("workday_id", "")
        _LOGGER.info(f"Delete workday {workday_id}")
        response = await self._workday_handler.delete_workday(workday_id=workday_id)
        return response

    async def get_process_steps(self, request, user_info):
        process_id = request.match_info.get("process_id", "")
        response = await self._process_handler.get_steps(process_id)
        return response

    async def get_steps(self, request, user_info):
        season_id = request.rel_url.query.get("season_id", None)
        filter_data = {}
        filter_data["season_id"] = season_id
        return await self._step_handler.get_steps(filter_data)

    async def upload_file(self, request, user_info):
        data = await request.post()
        file = data.get("file")
        if file is None:
            return ApiBadRequest("File is required")
        file_name = file.filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join("./static/uploaded", timestamp + file_name)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        domain = config.get("domain") or "http://localhost:8080"

        # TODO: uploaf file to blockchain server
        return success({
            "file_path": file_path[2:], 
            "url": f"{domain}/{file_path[2:]}",
            "name": file_path.split("/")[-1],
        })


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest('Improper JSON format')


def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise ApiBadRequest(
                "'{}' parameter is required".format(field))
