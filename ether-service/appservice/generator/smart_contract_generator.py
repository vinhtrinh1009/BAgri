import os
import json

from jinja2 import Environment, FileSystemLoader
# from generator import sdk_generator
from worker.tasks import migrate_contract
from constants.config import *
from includes import utils



def gen_code(data_rendering, dapp_user_folder, dapp_info, user_info, is_update, reply_to):
    file_loader = FileSystemLoader(os.path.join(base_dir, 'templates/'))

    env = Environment(loader=file_loader, autoescape=True)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    dapp_name = data_rendering['basic_info']['dapp_name']
    network_id = data_rendering['basic_info']['network_id']
    user_info = data_rendering['user_info']
    deploy_enviroment_path = os.path.join(base_dir, f'{dapp_user_folder}/{dapp_name}')

    if not os.path.exists(os.path.join(base_dir, f'{dapp_user_folder}')):
        os.mkdir(os.path.join(base_dir, f'{dapp_user_folder}'))
    if not os.path.exists(deploy_enviroment_path):
        os.mkdir(deploy_enviroment_path)
    if not os.path.exists(f'{deploy_enviroment_path}/contracts'):
        os.mkdir(f'{deploy_enviroment_path}/contracts')
    if not os.path.exists(f'{deploy_enviroment_path}/migrations'):
        os.mkdir(f'{deploy_enviroment_path}/migrations')

    os.system(
        "\cp "
        + os.path.join(base_dir, f"templates/deployment_enviroment")
        + "/truffle-config.js "
        + deploy_enviroment_path
        + "/truffle-config.js"
    )

    os.system(
        "\cp "
        + os.path.join(base_dir, f"templates/deployment_enviroment")
        + "/.gitignore "
        + deploy_enviroment_path
        + "/.gitignore"
    )
    
    contract = f'{deploy_enviroment_path}/contracts/{dapp_name}.sol'
    contract_template = env.get_template('smart_contract.jinja2')
    utils.gen_file(data=data_rendering, dst=contract, template=contract_template)

    contract_migration = f'{deploy_enviroment_path}/migrations/1_initial_{dapp_name}.js'
    contract_migration_template = env.get_template('migration.jinja2')
    utils.gen_file(data=data_rendering, dst=contract_migration, template=contract_migration_template)

    contract_address = migrate_contract.delay(deploy_enviroment_path = deploy_enviroment_path,
                                                dapp_name = dapp_name,
                                                user_info = user_info,
                                                network_id = network_id,
                                                data_rendering = data_rendering,
                                                dapp_user_folder = dapp_user_folder,
                                                dapp_info=dapp_info,
                                                is_update = is_update,
                                                reply_to=reply_to)



    