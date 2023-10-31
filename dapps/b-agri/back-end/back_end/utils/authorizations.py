from .response import ApiBadRequest


def only_manager(handler):
    async def check_user_is_manager(self, request, user_info):
        # if user_info["role"] != "qlv":
        #     return ApiBadRequest("Only manager (qlv) can access this API")
        return await handler(self, request, user_info)
    return check_user_is_manager


def only_technician(handler):
    async def check_user_is_technician(self, request, user_info):
        # if user_info["role"] != "ktv":
        #     return ApiBadRequest("Only technican (ktv) can access this API")
        return await handler(self, request, user_info)
    return check_user_is_technician
