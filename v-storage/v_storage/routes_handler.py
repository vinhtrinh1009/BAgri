import json
from json.decoder import JSONDecodeError
from utils.response import success, ApiBadRequest
from utils.logging import get_logger
import aiohttp
from aiohttp import web
from folder.routes_handler import FolderHandler
from file.routes_handler import FileHandler

_LOGGER = get_logger(__name__)

class RouteHandler:
    def __init__(self, database):
        self._folder_handler = FolderHandler(database)
        self._file_handler = FileHandler(database)

    # General
    async def get_shares(self, request, user_info):
        _LOGGER.info("Get share with me")
        response = await self._folder_handler.get_shares(user_info=user_info)
        return response

    async def get_child_shares(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Get child share with me of {folder_id}")
        response = await self._folder_handler.get_child_shares(folder_id=folder_id, user_info=user_info)
        return response

    async def get_recents(self, request, user_info):
        _LOGGER.info("Get recent")
        response = await self._folder_handler.get_recents(user_info=user_info)
        return response

    async def get_favorites(self, request, user_info):
        _LOGGER.info("Get favorite")
        response = await self._folder_handler.get_favorites(user_info=user_info)
        return response

    async def get_trashes(self, request, user_info):
        _LOGGER.info("Get trash")
        response = await self._folder_handler.get_trashes(user_info=user_info)
        return response

    async def get_child_trashes(self, request, user_info):
        _LOGGER.info(f"Get child trashes of {folder_id}")
        response = await self._folder_handler.get_child_trashes(folder_id=folder_id, user_info=user_info)
        return response

    async def get_user_folders(self, request, user_info):
        _LOGGER.info("Get user folders")
        response = await self._folder_handler.get_user_folders(user_info=user_info)
        return response
    
    async def recover_all(self, request, user_info):
        _LOGGER.info("Recover all")
        response = await self._folder_handler.recover_all(user_info=user_info)
        return response

    async def delete_all(self, request, user_info):
        _LOGGER.info("Delete all")
        response = await self._folder_handler.delete_all(user_info=user_info)
        return response

    # Folder
    async def get_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Get folder {folder_id}")
        labels = {
            "viewed": False
        }
        if "favorited" in request.rel_url.query:
            if request.rel_url.query["favorited"] == "True" or request.rel_url.query["favorited"] == "true":
                labels["favorited"] = True
            else:
                labels["favorited"] = False

        if "trashed" in request.rel_url.query:
            if request.rel_url.query["trashed"] == "True" or request.rel_url.query["trashed"] == "true":
                labels["trashed"] = True
            else:
                labels["trashed"] = False
        else:
            labels["trashed"] = False

        if "restricted" in request.rel_url.query:
            if request.rel_url.query["restricted"] == "True" or request.rel_url.query["restricted"] == "true":
                labels["restricted"] = True
            else:
                labels["restricted"] = False
        else:
            labels["restricted"] = False
        
        response = await self._folder_handler.get_folder(folder_id=folder_id, labels=labels, user_info=user_info)
        return response

    async def create_folder(self, request, user_info):
        _LOGGER.info("Create a new folder")
        body = await decode_request(request)
        required_fields = ["name", "parent_id"]
        validate_fields(required_fields, body)
        response = await self._folder_handler.create_folder(body=body, user_info=user_info)
        return response

    async def upload_folder(self, request, user_info):
        parent_id = request.match_info.get("folder_id", "")
        _LOGGER.info("Upload a new folder")
        response = await self._folder_handler.upload_folder(request=request, parent_id=parent_id, user_info=user_info)
        return response

    async def download_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Download folder {folder_id}")
        response = await self._folder_handler.download_folder(folder_id=folder_id, user_info=user_info)
        return response

    async def rename_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Rename folder {folder_id}")
        body = await decode_request(request)
        required_fields = ["name"]
        validate_fields(required_fields, body)
        new_folder_name = body["name"]
        response = await self._folder_handler.rename_folder(folder_id=folder_id, new_folder_name=new_folder_name, user_info=user_info)
        return response

    async def move_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Move folder {folder_id}")
        body = await decode_request(request)
        required_fields = ["parent_id"]
        validate_fields(required_fields, body)
        destination_parent_id = body["parent_id"]
        response = await self._folder_handler.move_folder(folder_id=folder_id, destination_parent_id=destination_parent_id, user_info=user_info)
        return response

    async def copy_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Copy folder {folder_id}")
        body = await decode_request(request)
        required_fields = ["parent_id"]
        validate_fields(required_fields, body)
        destination_parent_id = body["parent_id"]
        response = await self._folder_handler.copy_folder(folder_id=folder_id, destination_parent_id=destination_parent_id, user_info=user_info)
        return response

    async def favorite_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Favorite folder {folder_id}")
        # body = await decode_request(request)
        # required_fields = []
        # validate_fields(required_fields, body)
        response = await self._folder_handler.favorite_folder(folder_id=folder_id, user_info=user_info)
        return response

    async def unfavorite_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Unfavorite folder {folder_id}")
        response = await self._folder_handler.unfavorite_folder(folder_id=folder_id, user_info=user_info)
        return response

    async def trash_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Trash folder {folder_id}")
        response = await self._folder_handler.trash_folder(folder_id=folder_id, user_info=user_info)
        return response

    async def untrash_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Untrash folder {folder_id}")
        response = await self._folder_handler.untrash_folder(folder_id=folder_id, user_info=user_info)
        return response

    async def delete_folder(self, request, user_info):
        folder_id = request.match_info.get("folder_id", "")
        _LOGGER.info(f"Delete folder {folder_id}")
        response = await self._folder_handler.delete_folder(folder_id=folder_id, user_info=user_info)
        return response
        

    #=========================================================================#

    # File
    async def get_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Get file {file_id}")
        response = await self._file_handler.get_file(file_id=file_id, user_info=user_info)
        return response

    async def upload_file(self, request, user_info):
        parent_id = request.match_info.get("folder_id", "")
        _LOGGER.info("Upload a new file")
        response = await self._file_handler.upload_file(request=request, parent_id=parent_id, user_info=user_info)
        return response

    async def download_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Download file {file_id}")
        response = await self._file_handler.download_file(file_id=file_id, user_info=user_info)
        return response

    async def rename_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Rename file {file_id}")
        body = await decode_request(request)
        required_fields = ["name"]
        validate_fields(required_fields, body)
        new_file_name = body["name"]
        response = await self._file_handler.rename_file(file_id=file_id, new_file_name=new_file_name, user_info=user_info)
        return response

    async def move_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Move file {file_id}")
        body = await decode_request(request)
        required_fields = ["parent_id"]
        validate_fields(required_fields, body)
        destination_parent_id = body["parent_id"]
        response = await self._file_handler.move_file(file_id=file_id, destination_parent_id=destination_parent_id, user_info=user_info)
        return response

    async def copy_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Copy file {file_id}")
        body = await decode_request(request)
        required_fields = ["parent_id"]
        validate_fields(required_fields, body)
        destination_parent_id = body["parent_id"]
        response = await self._file_handler.copy_file(file_id=file_id, destination_parent_id=destination_parent_id, user_info=user_info)
        return response

    async def favorite_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Favorite file {file_id}")
        response = await self._file_handler.favorite_file(file_id=file_id, user_info=user_info)
        return response

    async def unfavorite_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Unfavorite file {file_id}")
        response = await self._file_handler.unfavorite_file(file_id=file_id, user_info=user_info)
        return response

    async def trash_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Trash file {file_id}")
        response = await self._file_handler.trash_file(file_id=file_id, user_info=user_info)
        return response

    async def untrash_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Untrash file {file_id}")
        response = await self._file_handler.untrash_file(file_id=file_id, user_info=user_info)
        return response

    async def delete_file(self, request, user_info):
        file_id = request.match_info.get("file_id", "")
        _LOGGER.info(f"Delete file {file_id}")
        response = await self._file_handler.delete_file(file_id=file_id, user_info=user_info)
        return response

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