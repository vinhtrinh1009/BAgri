import os
from platform import processor

import includes.git_handler as git_handler
from constants import BASE_DIR
from config.logging_config import get_logger
from settings import config as cfg
from generator import resource_generator

_LOGGER = get_logger(__name__)

async def gen_resource(resource_info, user_info, number_peer, public_ip, dapps, dst_folder):
    data = {
        "resource_info": resource_info,
        "user_info": user_info,
        "number_peer": number_peer,
        "public_ip": public_ip,
        "dapps": dapps
    }
    resource_generator.gen_code(data = data, dst_folder=dst_folder)
    _LOGGER.debug(f"Generated all file of resource: {resource_info['resource_name']}")
