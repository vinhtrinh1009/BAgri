from bson.errors import InvalidId
from bson.objectid import ObjectId
from utils.logging import get_logger
from utils.response import ApiInternalError, ApiNotFound, success

_LOGGER = get_logger(__name__)

class TreeHandler:
    def __init__(self, database, sdk):
        self.__database = database
        self.__sdk = sdk

    async def get_trees(self):
        trees = await self.__database.conn.tree.find({}).to_list(length=None)
        for tree in trees:
            tree["tree_id"] = str(tree["_id"])
            del tree["_id"]
        return success({
            "trees":  trees
        }) 

    async def get_tree(self, tree_id):
        try:
            tree = await self.__database.conn.tree.find_one({"_id": ObjectId(tree_id)})
            if tree is None:
                return ApiNotFound("Tree not found")

            tree["tree_id"] = str(tree["_id"])
            del tree["_id"]
            return success({
                "tree": tree
            })
        except InvalidId:
            return ApiNotFound("Tree not found")
        except Exception as e:
            _LOGGER.error(e)
            return ApiInternalError("Internal error")

    async def create_tree(self, new_tree):
        try:
            tree = await self.__database.conn.tree.insert_one(new_tree)
            new_tree["tree_id"] = str(tree.inserted_id)
            new_tree.pop("_id")
            self.__sdk.create_tree(new_tree["tree_id"], new_tree["name"], new_tree["description"], "")
            return success({
                "tree": new_tree
            })
        except Exception as e:
            _LOGGER.error(e)
            return ApiInternalError("Internal error")

    async def update_tree(self, tree_id, update_tree):
        try:
            updated_tree = await self.__database.conn.tree.find_one_and_update(
                    {"_id": ObjectId(tree_id)}, 
                    {"$set": update_tree},
                    return_document=True
            )
            if not updated_tree:
                return ApiNotFound("Tree not found")
            updated_tree["tree_id"] = str(updated_tree["_id"])
            del updated_tree["_id"]
            return success({
                "updated_tree": updated_tree
            })
        except InvalidId:
            return ApiNotFound("Tree not found")

    async def delete_tree(self, tree_id):
        try:
            deleted_tree = await self.__database.conn.tree.find_one_and_delete(
                    {"_id": ObjectId(tree_id)}
            )
            if not deleted_tree:
                return ApiNotFound("Tree not found")

            return success({
                "tree_id": tree_id
            })
        except InvalidId:
            return ApiNotFound("Tree not found")
