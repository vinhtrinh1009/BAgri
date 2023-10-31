import os
import asyncio
import datetime
import subprocess
from aiohttp import web
from settings import DATA_DIR
from bson.objectid import ObjectId
from file.action import FileAction
from folder.type import FolderType
from folder.action import FolderAction
from utils.logging import get_logger
from utils.response import success, ApiBadRequest, ApiInternalError
from utils.handle_ipfs import *

_LOGGER = get_logger(__name__)

class FolderHandler:
    def __init__(self, database):
        self.__database = database

    async def get_shares(self, user_info):
        try:
            filter = {
                "shared": {
                    "$in": [user_info["user_id"]]
                },
                "labels.trashed": False,
                "labels.restricted": False 
            }
            shared_folders = await self.__database.get_folders(folder_filter=filter)
            root_shared_folders = []
            for shared_folder in shared_folders:
                if all(folder["folder_id"] != shared_folder["parent_id"] for folder in shared_folders):
                    shared_folder["path"] = [
                        {
                            "folder_id": "",
                            "name": "Platform artifact"
                        },
                        {
                            "folder_id": shared_folder["folder_id"],
                            "name": shared_folder["name"]
                        }
                    ]
                    root_shared_folders.append(shared_folder)
                    
            shared_files = await self.__database.get_files(file_filter=filter)
            root_shared_files = []
            for shared_file in shared_files:
                if all(folder["folder_id"] != shared_file["parent_id"] for folder in shared_folders):
                    shared_file["path"] = [
                        {
                            "folder_id": "",
                            "name": "Platform artifact"
                        },
                        {
                            "file_id": shared_file["file_id"],
                            "name": f'{shared_file["name"]}{shared_file["ext_name"]}'
                        }
                    ]
                    root_shared_files.append(shared_file)

            return success({
                "shared_folders": root_shared_folders,
                "shared_files": root_shared_files
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def get_child_shares(self, folder_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, True))
            folder = folder[0]

            filter = {
                "shared": {
                    "$in": [user_info["user_id"]]
                },
                "path": {
                    "$in": [folder_id]
                },
                "labels.trashed": False,
                "labels.restricted": False 
            }

            parent_shared_folders = await self.__database.get_folders(folder_filter=filter)
            path = [{   
                "folder_id": "",
                "name": "Platform artifact"
            }]
                
            for folder_id_in_path in folder["path"]:
                filter = {
                    "_id": ObjectId(folder_id_in_path),
                    "shared": {
                        "$in": [user_info["user_id"]]
                    },
                    "labels.trashed": False,
                    "labels.restricted": False 
                }
                folder_in_paths = await self.__database.get_folders(folder_filter=filter)
                if len(folder_in_paths) == 1:
                    path.append({
                        "folder_id": folder_id_in_path,
                        "name": folder_in_paths[0]["name"]
                    })

            folder["path"] = path
                
            filter = {
                "shared": {
                    "$in": [user_info["user_id"]]
                },
                "parent_id": folder_id,
                "labels.trashed": False,
                "labels.restricted": False 
            }
            shared_folders = await self.__database.get_folders(folder_filter=filter)
            for shared_folder in shared_folders:
                shared_folder["path"] = path + [{
                    "folder_id": shared_folder["folder_id"],
                    "name": shared_folder["name"]
                }]

            shared_files = await self.__database.get_files(file_filter=filter)
            for shared_file in shared_files:
                shared_file["path"] = path + [{
                    "file_id": shared_file["file_id"],
                    "name": f'{shared_file["name"]}{shared_file["ext_name"]}'
                }]

            folder["shared_folders"] = shared_folders
            folder["shared_files"] = shared_files

            return success({
                "folder": folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def get_recents(self, user_info):
        try:
            folder_activity_filter = {
                "actor.user_id": user_info["user_id"],
                "type": "folder"
            }

            recent_folder_activities = await self.__database.get_activities(activity_filter=folder_activity_filter)
            recent_folders = []
            for folder in recent_folder_activities:
                try:
                    tmp_folder = await asyncio.gather(self.verify_folder(folder["target"], user_info, False))
                    recent_folders.append(tmp_folder[0])
                except:
                    pass

            file_filter = {
                "actor.user_id": user_info["user_id"],
                "type": "file"
            }
            
            recent_file_activities = await self.__database.get_activities(activity_filter=file_filter)
            recent_files = []
            for file in recent_file_activities:
                try:
                    tmp_file = await asyncio.gather(self.verify_file(file_id=file["target"], user_info=user_info, require_share=False))
                    recent_files.append(tmp_file[0])
                except:
                    pass

            return success({
                "recent_folders": recent_folders,
                "recent_files": recent_files
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def get_favorites(self, user_info):
        try:
            filter = {
                "owner.user_id": user_info["user_id"],
                "labels.favorited": True,
                "labels.trashed": False,
                "labels.restricted": False
            }
            favorited_folders = await self.__database.get_folders(folder_filter=filter)
            # for favorited_folder in favorited_folders:
            #     favorited_folder["path"] = await asyncio.gather(self.get_path(favorited_folder["path"], is_file_path=False))
                # favorited_folder["path"] = paths
            favorited_files = await self.__database.get_files(file_filter=filter)
            # for favorited_file in favorited_files:
            #     paths = await asyncio.gather(self.get_path(favorited_file["path"], is_file_path=True))
            #     favorited_file["path"] = paths

            return success({
                "favorited_folders": favorited_folders,
                "favorited_files": favorited_files
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def get_trashes(self, user_info):
        try:
            filter = {
                "owner.user_id": user_info["user_id"],
                "labels.trashed": True
            }
            trashed_folders = await self.__database.get_folders(folder_filter=filter)
            trashed_files = await self.__database.get_files(file_filter=filter)

            return success({
                "trashed_folders": trashed_folders,
                "trashed_files": trashed_files
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def get_child_trashes(self, folder_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, True))
            folder = folder[0]

            filter = {
                "owner.user_id": user_info["user_id"],
                "labels.trashed": False,
                "labels.restricted": True,
                "parent_id": folder_id
            }
            trashed_folders = await self.__database.get_folders(folder_filter=filter)
            trashed_files = await self.__database.get_files(file_filter=filter)

            folder["trashed_child_folders"] = trashed_folders
            folder["trashed_child_files"] = trashed_files

            return success({
                "folder": folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def recover_all(self, user_info):
        try:
            filter = {
                "owner.user_id": user_info["user_id"],
                "labels.trashed": True
            }

            modification = {
                "labels.trashed": False
            }

            await self.__database.update_folders(folder_filter=filter, modification=modification)
            await self.__database.update_files(file_filter=filter, modification=modification)

            filter = {
                "owner.user_id": user_info["user_id"],
                "labels.restricted": True
            }

            modification = {
                "labels.restricted": False
            }

            await self.__database.update_folders(folder_filter=filter, modification=modification)
            await self.__database.update_files(file_filter=filter, modification=modification)

            return success({
                "status": "done"
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def delete_all(self, user_info):
        try:
            filter = {
                "owner.user_id": user_info["user_id"],
                "labels.trashed": True
            }

            delete_files = await self.__database.get_files(file_filter=filter)
            for delete_file in delete_files:
                file_with_same_cid = await self.__database.get_files(file_filter={"cid": delete_file["cid"]})
                if len(file_with_same_cid) == 1:
                    await delete_file_on_ipfs(file_cid=delete_file["cid"])

            await self.__database.delete_folder(folder_filter=filter)
            await self.__database.delete_file(file_filter=filter)

            filter = {
                "owner.user_id": user_info["user_id"],
                "labels.restricted": True
            }

            restricted_files = await self.__database.get_files(file_filter=filter)
            for restricted_file in restricted_files:
                file_with_same_cid = await self.__database.get_files(file_filter={"cid": restricted_file["cid"]})
                if len(file_with_same_cid) < 2:
                    await delete_file_on_ipfs(file_cid=restricted_file["cid"])

            await self.__database.delete_folder(folder_filter=filter)
            await self.__database.delete_file(file_filter=filter)

            return success({
                "status": "done"
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def get_user_folders(self, user_info):
        try:
            filter = {
                "owner.user_id": user_info["user_id"],
                "type": FolderType.MY_STORAGE_ROOT.name
            }

            user_root_folders = await self.__database.get_folders(folder_filter=filter)
            if len(user_root_folders) == 0:
                new_folder = {
                    "name": user_info["username"],
                    "parent_id": "root",
                    "type": FolderType.MY_STORAGE_ROOT.name,
                    "owner": {
                        "user_id": user_info["user_id"],
                        "username": user_info["username"],
                        "full_name": user_info["full_name"]
                    },
                    "shared": [],
                    "path": [],
                    "labels": {
                        "favorited": False,
                        "trashed": False,
                        "restricted": False,
                        "viewed": False
                    }
                }
                folder_id = await self.__database.create_folder(new_folder)
                modification = {
                    "path": [folder_id]
                }

                user_root_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(folder_id)}, modification={"path": [folder_id]})
            else:
                user_root_folder = user_root_folders[0]
            filter = {
                "parent_id": user_root_folder["folder_id"],
                "owner.user_id": user_info["user_id"],
                "labels.trashed": False,
                "labels.restricted": False,
            }
            child_folders = await self.__database.get_folders(folder_filter=filter)
            child_files = await self.__database.get_files(file_filter=filter)

            user_root_folder["child_folders"] = child_folders
            user_root_folder["child_files"] = child_files

            user_root_folder["path"] = [{
                "folder_id": user_root_folder["folder_id"],
                "name": "My storage"
            }]

            filter = {
                "owner.user_id": user_info["user_id"]
            }

            user_files = await self.__database.get_files(file_filter=filter)
            user_root_folder["total_size"] = 0
            for file in user_files:
                user_root_folder["total_size"] += file["size"]

            return success({
                "user_folder": user_root_folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def get_folder(self, folder_id, labels, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, True))
            folder = folder[0]
            filter = {
                "parent_id": folder_id,
                "owner.user_id": user_info["user_id"],
                "labels.trashed": labels["trashed"],
                "labels.restricted": labels["restricted"],
            }

            if "favorited" in labels:
                filter["labels.favorited"] = labels["favorited"]
            child_folders = await self.__database.get_folders(folder_filter=filter)
            child_files = await self.__database.get_files(file_filter=filter)

            folder["child_folders"] = child_folders
            folder["child_files"] = child_files
            
            paths = []

            for path in folder["path"]:
                filter = {
                    "_id": ObjectId(path)
                }
                folders = await self.__database.get_folders(folder_filter=filter)
                paths.append({
                    "folder_id": path,
                    "name": 'My storage' if folders[0]['type'] == FolderType.MY_STORAGE_ROOT.name else folders[0]["name"]
                })
            folder["path"] = paths            

            return success({
                "folder": folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def create_folder(self, body, user_info):
        try:
            new_folder = {
                "name": body["name"],
                "parent_id": body["parent_id"],
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

            if "shared" in body:
                new_folder["shared"] = body["shared"]

            if body["parent_id"] == "root":
                new_folder["type"] = FolderType.MY_STORAGE_ROOT.name
                new_folder["shared"] = []
            else:
                new_folder["type"] = FolderType.STANDARD_FOLDER.name
            
            folder_id = await self.__database.create_folder(new_folder)

            modification = {}
            if body["parent_id"] == "root":
                modification["path"] = [folder_id]
            else:
                parent_folder = await asyncio.gather(self.verify_folder(new_folder["parent_id"], user_info, require_share=False))
                modification["path"] = parent_folder[0]["path"] + [folder_id]

            created_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(folder_id)}, modification=modification)

            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": created_folder["folder_id"],
                "action": FolderAction.CREATE.name,
                "type": "folder",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)

            return success({
                "folder": created_folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def upload_folder(self, request, parent_id, user_info):
        try:
            num_uploaded_folder = 0
            num_uploaded_file = 0
            root_folder_id = None

            parent_folder = await asyncio.gather(self.verify_folder(parent_id, user_info, require_share=False))

            type = FolderType.STANDARD_FOLDER.name

            owner = {
                "user_id": user_info["user_id"],
                "username": user_info["username"],
                "full_name": user_info["full_name"]
            }

            shared = []

            labels = {
                "favorited": False,
                "trashed": False,
                "restricted": False,
                "viewed": False
            }

            os.chdir(DATA_DIR)
            os.system("rm -rf *")

            async for field in (await request.multipart()):
                if field.name == 'shared':
                    shared = await field.read(decode=True)
                    shared = shared.decode()

                if 'upload_folder' in field.name:
                    file_path = field.filename.split("/")
                    filename = file_path[-1]
                    file_path.pop()

                    folder_path = f"{DATA_DIR}/{'/'.join(file_path)}"
                    
                    os.system(f"mkdir -p {folder_path}")
                    with open(f'{folder_path}/{filename}', 'wb') as writer:
                        while True:
                            chunk = await field.read_chunk()
                            if not chunk:
                                break
                            writer.write(chunk)
                        writer.close()

            
            os.chdir(DATA_DIR)
            root_childs = os.listdir(DATA_DIR)
            for root_child in root_childs:
                if os.path.isdir(f"{DATA_DIR}/{root_child}"):
                    temp_folder = [
                        {
                            "name": root_child,
                            "parent_id": parent_id,
                            "type": type,
                            "path": parent_folder[0]["path"],
                            "owner": owner,
                            "shared": shared,
                            "labels": labels,
                            "local_path": root_child 
                        }
                    ]

                    while len(temp_folder) > 0:
                        current_folder = temp_folder[0]
                        current_path = current_folder["local_path"]
                        current_folder_id = ""
                        current_folder_id = await self.__database.create_folder({
                            "name": current_folder["name"],
                            "parent_id": current_folder["parent_id"],
                            "type": current_folder["type"],
                            "path": current_folder["path"],
                            "owner": current_folder["owner"],
                            "shared": current_folder["shared"],
                            "labels": current_folder["labels"]
                        })
                        modification = {
                            "path": current_folder["path"] + [current_folder_id]
                        }
                        current_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(current_folder_id)}, modification=modification)

                        if not root_folder_id:
                            root_folder_id = current_folder_id

                            new_activity = {
                                "actor": {
                                    "user_id": user_info["user_id"],
                                    "username": user_info["username"],
                                    "full_name": user_info["full_name"]
                                },
                                "target": current_folder["folder_id"],
                                "action": FolderAction.UPLOAD.name,
                                "type": "folder",
                                "datetime": str(datetime.datetime.now())
                            }

                            activity_id = await self.__database.create_activity(new_activity)

                        num_uploaded_folder += 1

                        current_childs = os.listdir(f'{DATA_DIR}/{current_path}')
                        for child_name in current_childs:
                            child_path = f'{DATA_DIR}/{current_path}/{child_name}'
                            if os.path.isdir(child_path):
                                temp_folder.append({
                                    "name": child_name,
                                    "parent_id": current_folder_id,
                                    "type": type,
                                    "path": current_folder["path"],
                                    "owner": owner,
                                    "shared": current_folder["shared"],
                                    "labels": labels,
                                    "local_path": f'{current_path}/{child_name}' 
                                })
                            else:
                                upload_file = {
                                    "size": os.stat(child_path).st_size,
                                    "parent_id": current_folder_id,
                                    "path": current_folder["path"],
                                    "owner": owner,
                                    "shared": current_folder["shared"],
                                    "labels": labels
                                }

                                upload_file["name"], upload_file["ext_name"] = os.path.splitext(child_name)
                                upload_file["name"] = upload_file["name"].replace(" ", "-")
                                upload_file["cid"] = await save_file_to_ipfs(child_path, f'{child_name}')

                                file_id = await self.__database.create_file(upload_file)

                                modification = {
                                    "path": upload_file["path"] + [file_id]
                                }

                                await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)

                                num_uploaded_file += 1

                        temp_folder = temp_folder[1:]

                else:
                    upload_file = {
                        "size": os.stat(f"{DATA_DIR}/{root_child}").st_size,
                        "parent_id": parent_id,
                        "path": parent_folder[0]["path"],
                        "owner": owner,
                        "shared": shared,
                        "labels": labels
                    }

                    upload_file["name"], upload_file["ext_name"] = os.path.splitext(root_child)
                    upload_file["name"] = upload_file["name"].replace(" ", "-")
                    upload_file["cid"] = await save_file_to_ipfs(f"{DATA_DIR}/{root_child}", root_child)

                    file_id = await self.__database.create_file(upload_file)

                    modification = {
                        "path": upload_file["path"] + [file_id]
                    }

                    await self.__database.update_file(file_filter={"_id": ObjectId(file_id)}, modification=modification)

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
                    
                    num_uploaded_file += 1

            os.chdir(DATA_DIR)
            os.system("rm -rf *")

            # modification = {
            #     "shared": shared
            # }

            # await self.__database.update_folder(folder_filter={"_id": ObjectId(root_folder_id)}, modification=modification)

            return success({
                "num_uploaded_folder": num_uploaded_folder,
                "num_uploaded_file": num_uploaded_file,
                "uploaded_folder_id": root_folder_id
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def download_folder(self, folder_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, require_share=True))

            folder[0]["local_path"] = f'{DATA_DIR}/{folder[0]["name"]}'

            os.chdir(DATA_DIR)
            os.system("rm -rf *")

            os.system(f"mkdir -p {DATA_DIR}/{folder[0]['name']}")
            queue_folders = [folder[0]]
            while (len(queue_folders) > 0):
                current_path = f"{queue_folders[0]['local_path']}"
                os.chdir(current_path)
                filter = {
                    "parent_id": queue_folders[0]["folder_id"],
                    "labels.trashed": False,
                    "labels.restricted": False
                }
                current_child_files = await self.__database.get_files(file_filter=filter)
                for child_file in current_child_files:
                    child_file["local_path"] = f'{current_path}/{child_file["name"]}{child_file["ext_name"]}'
                    await download_file_from_ipfs(child_file["cid"], child_file["local_path"])

                current_child_folders = await self.__database.get_folders(folder_filter=filter)
                for child_folder in current_child_folders:
                    child_folder["local_path"] = f'{current_path}/{child_folder["name"]}'
                    os.system(f"mkdir -p {child_folder['local_path']}")
                    queue_folders.append(child_folder)
                queue_folders = queue_folders[1:]

            os.chdir(DATA_DIR)
            os.system(f"zip -r {folder[0]['name']}.zip {folder[0]['name']}")
            os.system(f"rm -rf {folder[0]['name']}")
            # subprocess.run(args=["zip", "-r", f'{folder[0]["name"]}.zip', folder[0]["name"]],check=True)
            # subprocess.run(args=["rm", "-rf", folder[0]["name"]], check=True)

            return web.FileResponse(f'{DATA_DIR}/{folder[0]["name"]}.zip')
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def rename_folder(self, folder_id, new_folder_name, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, require_share=False))
            modification = {
                "name": new_folder_name
            }

            renamed_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(folder_id)}, modification=modification)

            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": renamed_folder["folder_id"],
                "action": FolderAction.RENAME.name,
                "type": "folder",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)

            return success({
                "renamed_folder": renamed_folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def move_folder(self, folder_id, destination_parent_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, require_share=False))
            destination_parent_folder = await asyncio.gather(self.verify_folder(destination_parent_id, user_info, require_share=False))

            if folder[0]["parent_id"] == destination_parent_id:
                raise Exception("Cannot move to present folder")

            temp_folders = [{
                "folder_id": folder_id,
                "path": destination_parent_folder[0]["path"] + [folder_id]
            }]

            temp_files = []

            while len(temp_folders) > 0:
                current_folder = temp_folders[0]
                modification = {
                    "path": current_folder["path"]
                }
                await self.__database.update_folder(folder_filter={"_id": ObjectId(current_folder["folder_id"])}, modification=modification)
                
                filter = {
                    "parent_id": current_folder["folder_id"]
                }
                current_child_folders = await self.__database.get_folders(folder_filter=filter)
                for current_child_folder in current_child_folders:
                    temp_folders.append({
                        "folder_id": current_child_folder["folder_id"],
                        "path": current_folder["path"] + [current_child_folder["folder_id"]],
                    })

                current_child_files = await self.__database.get_files(file_filter=filter)
                for current_child_file in current_child_files:
                    temp_files.append({
                        "file_id": current_child_file["file_id"],
                        "path": current_folder["path"] + [current_child_file["file_id"]]
                    })
                temp_folders = temp_folders[1:]
            
            for temp_file in temp_files:
                modification = {
                    "path": temp_file["path"]
                }
                await self.__database.update_file(file_filter={"_id": ObjectId(temp_file["file_id"])}, modification=modification)
            
            modification = {
                "parent_id": destination_parent_id
            }

            moved_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(folder_id)}, modification=modification)

            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": moved_folder["folder_id"],
                "action": FolderAction.MOVE.name,
                "type": "folder",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)

            return success({
                "moved_folder": moved_folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def copy_folder(self, folder_id, destination_parent_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, require_share=False))
            parent_folder_destination = await asyncio.gather(self.verify_folder(destination_parent_id, user_info, require_share=False))
            
            folder[0]["path"] = parent_folder_destination[0]["path"]
            folder[0]["parent_id"] = destination_parent_id

            temp_folders = [folder[0]]

            temp_files = []
            
            copied_folder_id = None

            while len(temp_folders) > 0:
                current_folder = temp_folders[0]
                old_folder_id = current_folder["folder_id"]
                current_folder.pop("folder_id", None)

                current_folder_id = await self.__database.create_folder(current_folder)
                modification = {
                    "path": current_folder["path"] + [current_folder_id]
                }
                updated_current_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(current_folder_id)}, modification=modification)

                if not copied_folder_id:
                    copied_folder_id = current_folder_id
                    new_activity = {
                        "actor": {
                            "user_id": user_info["user_id"],
                            "username": user_info["username"],
                            "full_name": user_info["full_name"]
                        },
                        "target": current_folder_id,
                        "action": FolderAction.COPY.name,
                        "type": "folder",
                        "datetime": str(datetime.datetime.now())
                    }

                    activity_id = await self.__database.create_activity(new_activity)

                filter = {
                    "parent_id": old_folder_id
                }
                current_child_folders = await self.__database.get_folders(folder_filter=filter)
                for current_child_folder in current_child_folders:
                    current_child_folder["path"] = updated_current_folder["path"]
                    current_child_folder["parent_id"] = updated_current_folder["folder_id"]
                    temp_folders.append(current_child_folder)

                current_child_files = await self.__database.get_files(file_filter=filter)
                for current_child_file in current_child_files:
                    current_child_file["path"] = updated_current_folder["path"]
                    current_child_file["parent_id"] = updated_current_folder["folder_id"]
                    temp_files.append(current_child_file)
                temp_folders = temp_folders[1:]

            for temp_file in temp_files:
                temp_file.pop("file_id", None)
                current_file_id = await self.__database.create_file(temp_file)

                modification = {
                    "path": temp_file["path"] + [current_file_id]
                }

                await self.__database.update_file(file_filter={"_id": ObjectId(current_file_id)}, modification=modification)

            return success({
                "status": "done"
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def favorite_folder(self, folder_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, require_share=False))
            modification = {
                "labels.favorited": True
            }

            favorited_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(folder_id)}, modification=modification)

            new_activity = {
                "actor": {
                    "user_id": user_info["user_id"],
                    "username": user_info["username"],
                    "full_name": user_info["full_name"]
                },
                "target": favorited_folder["folder_id"],
                "action": FolderAction.FAVORITE.name,
                "type": "folder",
                "datetime": str(datetime.datetime.now())
            }

            activity_id = await self.__database.create_activity(new_activity)

            return success({
                "favorited_folder": favorited_folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def unfavorite_folder(self, folder_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, require_share=False))
            modification = {
                "labels.favorited": False
            }

            unfavorited_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(folder_id)}, modification=modification)

            return success({
                "unfavorited_folder": unfavorited_folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def trash_folder(self, folder_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, require_share=False))
            modification = {
                "labels.trashed": True
            }

            trashed_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(folder_id)}, modification=modification)

            # Update child, nested child labels restricted = True
            modification = {
                "labels.restricted": True
            }

            filter = {
                "parent_id": folder_id,
                "labels.trashed": False
            }

            temp_folders = await self.__database.get_folders(folder_filter=filter)
            temp_files = await self.__database.get_files(file_filter=filter)

            while len(temp_folders) > 0:
                await self.__database.update_folder(folder_filter={"_id": ObjectId(temp_folders[0]["folder_id"])}, modification=modification)
                filter = {
                    "parent_id": temp_folders[0]["folder_id"],
                    "labels.restricted": False,
                    "labels.trashed": False
                }
                current_child_folders = await self.__database.get_folders(folder_filter=filter)
                current_child_files = await self.__database.get_files(file_filter=filter)
                temp_folders = temp_folders + current_child_folders
                temp_files = temp_files + current_child_files
                temp_folders = temp_folders[1:]
            for temp_file in temp_files:
                await self.__database.update_file(file_filter={"_id": ObjectId(temp_file["file_id"])}, modification=modification)

            # new_activity = {
            #     "actor": {
            #         "user_id": user_info["user_id"],
            #         "username": user_info["username"],
            #         "full_name": user_info["full_name"]
            #     },
            #     "target": trashed_folder["folder_id"],
            #     "action": FolderAction.TRASH.name,
            #     "type": "folder",
            #     "datetime": str(datetime.datetime.now())
            # }

            # activity_id = await self.__database.create_activity(new_activity)

            return success({
                "trashed_folder": trashed_folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def untrash_folder(self, folder_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, False))
            modification = {
                "labels.trashed": False
            }

            untrashed_folder = await self.__database.update_folder(folder_filter={"_id": ObjectId(folder_id)}, modification=modification)

            # Update child, nested child labels restricted = False
            modification = {
                "labels.restricted": False
            }

            filter = {
                "parent_id": folder_id,
                "labels.trashed": False,
                "labels.restricted": True
            }
            temp_folders = await self.__database.get_folders(folder_filter=filter)
            temp_files = await self.__database.get_files(file_filter=filter)


            while len(temp_folders) > 0:
                await self.__database.update_folder(folder_filter={"_id": ObjectId(temp_folders[0]["folder_id"])}, modification=modification)
                filter = {
                    "parent_id": temp_folders[0]["folder_id"],
                    "labels.trashed": False,
                    "labels.restricted": True
                }
                
                current_child_folders = await self.__database.get_folders(folder_filter=filter)
                current_child_files = await self.__database.get_files(file_filter=filter)
                temp_folders = temp_folders + current_child_folders
                temp_files = temp_files + current_child_files
                temp_folders = temp_folders[1:]
            for temp_file in temp_files:
                await self.__database.update_file(file_filter={"_id": ObjectId(temp_file["file_id"])}, modification=modification)

            # new_activity = {
            #     "actor": {
            #         "user_id": user_info["user_id"],
            #         "username": user_info["username"],
            #         "full_name": user_info["full_name"]
            #     },
            #     "target": folder_id,
            #     "action": FolderAction.UNTRASH.name,
            #     "type": "folder",
            #     "datetime": str(datetime.datetime.now())
            # }

            # activity_id = await self.__database.create_activity(new_activity)

            return success({
                "untrashed_folder": untrashed_folder
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def delete_folder(self, folder_id, user_info):
        try:
            folder = await asyncio.gather(self.verify_folder(folder_id, user_info, False))
            
            temp_folders = [
                {
                    "folder_id": folder_id
                }
            ]
            temp_files = []
            while len(temp_folders) > 0:
                filter = {
                    "parent_id": temp_folders[0]["folder_id"]
                }
                current_child_folders = await self.__database.get_folders(folder_filter=filter)
                current_child_files = await self.__database.get_files(file_filter=filter)
                
                temp_folders = temp_folders + current_child_folders
                temp_files = temp_files + current_child_files

                await self.__database.delete_folder(folder_filter={"_id": ObjectId(temp_folders[0]["folder_id"])})
                await self.__database.delete_activity(activity_filter={"target": temp_folders[0]["folder_id"]})

                temp_folders = temp_folders[1:]
            
            for temp_file in temp_files:
                file_with_same_cid = await self.__database.get_files(file_filter={"cid": temp_file["cid"]})
                if len(file_with_same_cid) < 2:
                    await delete_file_on_ipfs(file_cid=temp_file["cid"])
                await self.__database.delete_file(file_filter={"_id": ObjectId(temp_file["file_id"])})
                await self.__database.delete_activity(activity_filter={"target": temp_file["file_id"]})

            return success({
                "deleted_folder_id": folder_id
            })
        except Exception as error:
            _LOGGER.error(error, exc_info=True)
            return ApiInternalError(error.args[0])

    async def verify_folder(self, folder_id, user_info, require_share):
        if folder_id == 'root':
            raise Exception("You cannot to do this action")
        folder_filter = {
            "_id": ObjectId(folder_id)
        }
        folders = await self.__database.get_folders(folder_filter=folder_filter)

        if len(folders) == 0:
            raise Exception("Folder doesn't exist")
        
        folder = folders[0]
        # print(folder)
        # if folder["type"] == FolderType.MY_STORAGE_ROOT.name:
        #     raise Exception("You cannot to do this action")

        if folder["owner"]["user_id"] == user_info["user_id"] or (require_share == True and user_info["user_id"] in folder["shared"]):
            return folder
        else:
            raise Exception("You don't have permission to do this action!")

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