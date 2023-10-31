import os

from jinja2 import Environment, FileSystemLoader

from constants import BASE_DIR
from includes import utils
from config.logging_config import get_logger

_LOGGER = get_logger(__name__)


def gen_code(data, dst_folder):
    addresser_folder_sdk = os.path.join(
        BASE_DIR,
        '{0}/{1}/{2}sdk/addressing/'.format(dst_folder, data['basic_info']['dapp_name'], data['basic_info']['dapp_name'])
    )

    addresser_folder_processor = os.path.join(
        BASE_DIR,
        '{0}/{1}/{2}processor/addressing/'.format(dst_folder, data['basic_info']['dapp_name'], data['basic_info']['dapp_name'])
    )

    if not os.path.exists(addresser_folder_sdk):
        os.makedirs(addresser_folder_sdk)

    if not os.path.exists(addresser_folder_processor):
        os.makedirs(addresser_folder_processor)

    file_loader = FileSystemLoader(os.path.join(BASE_DIR, 'templates/addressing'))

    env = Environment(loader=file_loader, autoescape=True)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    addresser_sdk = addresser_folder_sdk + 'addresser.py'
    addresser_processor = addresser_folder_processor + 'addresser.py'

    addresser_template = env.get_template('addresser_template.jinja2')
    utils.gen_file(data=data, dst=addresser_processor, template=addresser_template)
    _LOGGER.debug(f"Generated addresser: {addresser_folder_processor}")
    utils.gen_file(data=data, dst=addresser_sdk, template=addresser_template)
    _LOGGER.debug(f"Generated addresser: {addresser_folder_sdk}")
