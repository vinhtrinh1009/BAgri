import os

from jinja2 import Environment, FileSystemLoader

from constants import BASE_DIR
from includes import utils
from config.logging_config import get_logger

_LOGGER = get_logger(__name__)

def gen_code(data, dst_folder):
    # create folder
    sdk_folder = os.path.join(
        BASE_DIR, '{0}/{1}/{2}sdk/'.format(dst_folder, data['basic_info']['dapp_name'], data['basic_info']['dapp_name']),
    )

    if not os.path.exists(sdk_folder):
        os.makedirs(sdk_folder)

    file_loader = FileSystemLoader(os.path.join(BASE_DIR, 'templates/sdk'))
    path = os.path.join(BASE_DIR, 'templates/sdk')

    os.system(f"cp {path}/requirements.txt {sdk_folder}")

    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    # Generate router_handler
    router_handler = sdk_folder + 'handler.py'
    router_handler_template = env.get_template('route_handler_template.jinja2')
    utils.gen_file(data=data, dst=router_handler, template=router_handler_template)

    # Generate messaging
    messaging = sdk_folder + 'messaging.py'
    messaging_template = env.get_template('messaging_template.jinja2')
    utils.gen_file(data=data, dst=messaging, template=messaging_template)

    # Generate transaction_creation
    transaction_creation = sdk_folder + 'transaction_creation.py'
    transaction_creation_template = env.get_template('transaction_creation_template.jinja2')
    utils.gen_file(data=data, dst=transaction_creation, template=transaction_creation_template)

    # Generate errors
    errors = sdk_folder + 'errors.py'
    errors_template = env.get_template('errors_template.jinja2')
    utils.gen_file(data=data, dst=errors, template=errors_template)

    # Generate encrypt
    if data['basic_info']['encryptionType'] == "AES":
        encrypt = sdk_folder + 'AES_encrypt.py'
        encrypt_template = env.get_template('AES_encrypt.jinja2')
        utils.gen_file(data=data, dst=encrypt, template=encrypt_template)
    
    else:
        encrypt = sdk_folder + 'RSA_encrypt.py'
        encrypt_template = env.get_template('RSA_encrypt.jinja2')
        utils.gen_file(data=data, dst=encrypt, template=encrypt_template)

    # Generate file_handler
    encrypt = sdk_folder + 'file_handler.py'
    encrypt_template = env.get_template('file_handler.jinja2')
    utils.gen_file(data=data, dst=encrypt, template=encrypt_template)

    _LOGGER.debug(f"Generate sdk: {sdk_folder}")
