import os
import datetime
import asyncio
import subprocess
from aiohttp import web
from settings import DATA_DIR
from bson.objectid import ObjectId
from file.action import FileAction
from utils.handle_ipfs import *
from utils.logging import get_logger
from utils.response import success, ApiBadRequest, ApiInternalError

_LOGGER = get_logger(__name__)

class FileHandler:
    def __init__(self, database):
        self.__database = database

    async def get_file(self, file_id, user_info):
        try:
            file_filter = {
                "_id": ObjectId(file_id)
            }
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            file = file[0]
            return success({
                "file": file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def upload_file(self, request, parent_id, user_info):
        try:
            parent_folder = await asyncio.gather(self.verify_folder(parent_id, user_info))

            upload_file = {
                "size": 0,
                "parent_id": parent_id,
                "path": [],
                "owner": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "shared": [],
                "labels": {
                    "favorited": False,
                    "trashed": False,
                    "restricted": False,
                    "viewed": False
                }
            }

            async for field in (await request.multipart()):
                if field.name == 'shared':
                    shared = await field.read(decode=True)
                    upload_file["shared"] = shared.decode()

                    
                if field.name == 'upload_file':
                    origin_name = field.filename
                    file_path = f'{DATA_DIR}/{origin_name}'
                    with open(file_path, 'wb') as writer:
                        while True:
                            chunk = await field.read_chunk()
                            if not chunk:
                                break
                            upload_file["size"] += len(chunk)
                            writer.write(chunk)
                        writer.close()

                    upload_file["name"], upload_file["ext_name"] = os.path.splitext(origin_name)
                    upload_file["name"] = upload_file["name"].replace(" ", "-")
                    upload_file["cid"] = await save_file_to_ipfs(file_path, f'{origin_name}') 

                    os.chdir(DATA_DIR)
                    os.system(f"rm -rf {file_path}")
            
            file_id = await self.__database.create_file(upload_file)

            modification = {
                "path": parent_folder[0]["path"] + [file_id]
            }

            uploaded_file = await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)

            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": file_id,
                "action": FileAction.UPLOAD.name,
                "type": "file",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)

            return success({
                "uploaded_file": uploaded_file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def download_file(self, file_id, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, True))
            file = file[0]

            os.chdir(DATA_DIR)
            os.system("rm -rf *")
            # subprocess.run(args=["rm", "-rf", "*"], check=True)

            file["local_path"] = f'{DATA_DIR}/{file["name"]}{file["ext_name"]}'
            await download_file_from_ipfs(file["cid"], file["local_path"])
            
            return web.FileResponse(f'{DATA_DIR}/{file["name"]}{file["ext_name"]}')
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def rename_file(self, file_id, new_file_name, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            modification = {
                "name": new_file_name.replace(" ", "-")
            }

            renamed_file = await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)
            
            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": file_id,
                "action": FileAction.RENAME.name,
                "type": "file",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)
            
            return success({
                "renamed_file": renamed_file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def move_file(self, file_id, destination_parent_id, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            destination_parent_folder = await asyncio.gather(self.verify_folder(destination_parent_id, user_info))
            if file[0]["parent_id"] == destination_parent_id:
                raise Exception("Cannot move to present folder")
            modification = {
                "path": destination_parent_folder[0]["path"] + [file_id],
                "parent_id": destination_parent_id
            }

            moved_file = await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)
            
            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": file_id,
                "action": FileAction.MOVE.name,
                "type": "file",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)

            return success({
                "moved_file": moved_file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def copy_file(self, file_id, destination_parent_id, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            destination_parent_folder = await asyncio.gather(self.verify_folder(destination_parent_id, user_info))
            
            file = file[0]

            file["parent_id"] = destination_parent_id
            file.pop("file_id", None)

            copied_file_id = await self.__database.create_file(file)
            
            modification = {
                "path": destination_parent_folder[0]["path"] + [file_id]
            }

            copied_file = await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)

            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": copied_file["file_id"],
                "action": FileAction.COPY.name,
                "type": "file",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)

            return success({
                "copied_file": copied_file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def favorite_file(self, file_id, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            modification = {
                "labels.favorited": True
            }

            favorited_file = await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)

            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": file_id,
                "action": FileAction.FAVORITE.name,
                "type": "file",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)

            return success({
                "favorited_file": favorited_file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def unfavorite_file(self, file_id, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            modification = {
                "labels.favorited": False
            }

            unfavorited_file = await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)

            # new_activity = {
            #     "actor": {
            #         "user_id": user_info["user_id"],
            #         "username": user_info["username"],
            #         "full_name": user_info["full_name"]
            #     },
            #     "target": file_id,
            #     "action": FileAction.UNFAVORITE.name,
            #     "type": "file",
            #     "datetime": str(datetime.datetime.now())
            # }

            # activity_id = await self.__database.create_activity(new_activity)

            return success({
                "unfavorited_file": unfavorited_file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def trash_file(self, file_id, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            modification = {
                "labels.trashed": True
            }

            trashed_file = await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)

            # new_activity = {
            #     "actor": {
            #         "user_id": user_info["user_id"],
            #         "username": user_info["username"],
            #         "full_name": user_info["full_name"]
            #     },
            #     "target": file_id,
            #     "action": FileAction.TRASH.name,
            #     "type": "file",
            #     "datetime": str(datetime.datetime.now())
            # }

            # activity_id = await self.__database.create_activity(new_activity)

            return success({
                "trashed_file": trashed_file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def untrash_file(self, file_id, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            modification = {
                "labels.trashed": False
            }

            untrashed_file = await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)

            # new_activity = {
            #     "actor": {
            #         "user_id": user_info["user_id"],
            #         "username": user_info["username"],
            #         "full_name": user_info["full_name"]
            #     },
            #     "target": file_id,
            #     "action": FileAction.UNTRASH.name,
            #     "type": "file",
            #     "datetime": str(datetime.datetime.now())
            # }

            # activity_id = await self.__database.create_activity(new_activity)

            return success({
                "untrashed_file": untrashed_file
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def delete_file(self, file_id, user_info):
        try:
            file = await asyncio.gather(self.verify_file(file_id, user_info, False))
            
            file_with_same_cid = await self.__database.get_files(file_filter={"cid": file[0]["cid"]})
            if len(file_with_same_cid) < 2:
                await delete_file_on_ipfs(file_cid=file[0]["cid"])
            await self.__database.delete_file(file_filter={"_id": ObjectId(file[0]["file_id"])})
            await self.__database.delete_activity(activity_filter={"target": file[0]["file_id"]})
            
            return success({
                "deleted_folder_id": file_id
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def verify_folder(self,folder_id, user_info):
        if folder_id == 'root':
            raise Exception("You cannot to do this action")
        folder_filter = {
            "_id": ObjectId(folder_id)
        }
        folders = await self.__database.get_folders(folder_filter=folder_filter)
        if len(folders) == 0:
            raise Exception("Folder doesn't exist")

        folder = folders[0]

        if folder["owner"]["user_id"] != user_info["user_id"]:
            raise Exception("You don't have permission to do this action!")

        return folder

    async def verify_file(self, file_id, user_info, require_share):
        if file_id == 'root':
            raise Exception("You cannot to do this action!")
        file_filter = {
            "_id": ObjectId(file_id)
        }
        files = await self.__database.get_files(file_filter=file_filter)
        if len(files) == 0:
            raise Exception("File doesn't exist!")

        file = files[0]

        if file["owner"]["user_id"] == user_info["user_id"] or (require_share == True and user_info["user_id"] in file["shared"]):
            return file
        else:
            raise Exception("You don't have permission to do this action!")