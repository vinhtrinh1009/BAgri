from __future__ import absolute_import, unicode_literals
import os
import time
import asyncio
import json

from kombu import Connection, Queue, Exchange, Consumer, Producer, exceptions
from .celery import app
import includes.git_handler as git_handle
from settings import config
from generator import sdk_generator
from celery.utils.log import get_task_logger

from config.logging_config import get_logger

from exceptions import ThirdPartyRequestError, NotSupported, ServiceError
from worker.syn_broker_client import BrokerClientSyn
from constants.config import *


_LOGGER = get_logger(__name__)
# _LOGGER = get_task_logger(__name__)

broker_client = BrokerClientSyn(username=config["rabbitmq"]["username"],
                                password=config["rabbitmq"]["password"],
                                host=config["rabbitmq"]["host"],
                                port=config["rabbitmq"]["port"])


@app.task
def migrate_contract(deploy_enviroment_path, dapp_name, user_info, network_id, data_rendering, dapp_user_folder, dapp_info, is_update, reply_to):
    deployment_output = os.popen(
        f'cd {deploy_enviroment_path} && npm install truffle @truffle/hdwallet-provider@1.2.3 && truffle migrate --network {network_id}'
    ).read()
    print('===== deployment_output =====')
    print("deployment: ", deployment_output)
    print('=== end deployment_output ===')
    
    contract_address = deployment_output.split('>>>')[1]

    os.chdir(f'{deploy_enviroment_path}')

    cmd = (
        "rm -rf node_modules"
    )

    os.system(cmd)

    sdk_path = os.path.join(base_dir, 
                        f'{dapp_user_folder}/{dapp_name}_sdk')

    if not os.path.exists(sdk_path):
        os.mkdir(sdk_path)
        os.mkdir(sdk_path + '/build')
        os.mkdir(sdk_path + '/contracts')

    os.system(
        '\cp '
        + deploy_enviroment_path 
        + f'/build/contracts/{dapp_name.capitalize()}.json '
        + sdk_path
        + f'/build/{dapp_name}.json'
    )

    os.system(
        '\cp '
        + deploy_enviroment_path 
        + f'/contracts/{dapp_name}.sol '
        + sdk_path
        + f'/contracts/{dapp_name}.sol'
    )
    data_rendering["contract_address"] = contract_address

    smart_contract_path = os.path.join(base_dir,
                                  f'{dapp_user_folder}/{dapp_info["dapp_name"]}/')
    smart_contract_project_name = dapp_info["dapp_name"] + "_smart_contract"

    # generate sdk 
    sdk_generator.gen_code(data_rendering, sdk_path)

    sdk_path = os.path.join(base_dir, f'{dapp_user_folder}/{dapp_info["dapp_name"]}_sdk/')
    sdk_project_name = dapp_info["dapp_name"] + "_sdk"

    if is_update:
        git_push_without_create.delay(dapp_info=dapp_info,
                                      user_info=user_info,
                                      sdk_path=sdk_path,
                                      smart_contract_path=smart_contract_path,
                                      commit_message="Update DApp",
                                      reply_to=reply_to)
    else:
        git_push.delay(dapp_info=dapp_info,
                    user_info=user_info,
                    smart_contract_path=smart_contract_path,
                    smart_contract_project_name=smart_contract_project_name,
                    sdk_path=sdk_path,
                    sdk_project_name=sdk_project_name,
                    commit_message="Create DApp",
                    reply_to=reply_to)

    
@app.task
def git_delete_group(dapp_info, user_info, reply_to):
    user_groups = git_handle.get_groups(user_info["username"], config["gitlab"]["dapp_group_id"])
    if len(user_groups) == 1:
        user_group_id = user_groups[0]["id"]
    elif len(user_groups) == 0:
        _LOGGER.debug(f"There are no groups on gitlab with name: {user_info['username']}")
        raise ServiceError(f"There are no groups on gitlab with name: {user_info['username']}")
    else:
        _LOGGER.debug(f"Have many groups on gitlab with name: {user_info['username']}")
        raise ServiceError(f"Have many groups on gitlab with name: {user_info['username']}")

    
    dapp_groups = git_handle.get_groups(dapp_info["dapp_name"], user_group_id)

    if len(dapp_groups) == 1:
        dapp_group_id = dapp_groups[0]["id"]
    elif len(dapp_groups) == 0:
        _LOGGER.error(f"There are no groups on gitlab with name: {dapp_info['dapp_name']}")
        raise ServiceError(f"There are no groups on gitlab with name: {dapp_info['dapp_name']}")
    else:
        _LOGGER.error(f"Have many groups on gitlab with name: {dapp_info['dapp_name']}")
        raise ServiceError(f"Have many groups on gitlab with name: {dapp_info['dapp_name']}")

    try:
        git_handle.delete_group(dapp_group_id)
        _LOGGER.info((f"Delete DApp on gitlab with name '{dapp_info['dapp_name']}' successfully"))
        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_info["dapp_id"]
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=json.dumps(success_message))

    except:
        _LOGGER.error(f"Error while delete DApp on gitlab with name: {dapp_info['dapp_name']}")
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_info["dapp_id"]
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=json.dumps(failure_message))


@app.task
def git_push_without_create(dapp_info, user_info, sdk_path, smart_contract_path, commit_message, reply_to):

    cmd = (
            "cd "
            + sdk_path
            + " && git add . && git commit -m '"
            + commit_message
            + "' && git push"
    )
    os.system(cmd)
    cmd = (
            "cd "
            + smart_contract_path
            + " && git add . && git commit -m '"
            + commit_message
            + "' && git push"
    )
    os.system(cmd)

    success_message = {
        "data": {
            "user_id": user_info["user_id"],
            "dapp_id": dapp_info["dapp_id"]
        }
    }

    _LOGGER.info(success_message)
    broker_client.publish_messages(routing_key=reply_to, message=json.dumps(success_message))

@app.task
def git_push(
        dapp_info,
        user_info,
        smart_contract_path,
        smart_contract_project_name,
        sdk_path,
        sdk_project_name,
        commit_message,
        reply_to
):
    username = user_info["username"]
    dapp_name=dapp_info["dapp_name"]
    network_id=dapp_info["network_id"]

    user_groups = git_handle.get_groups(username, config['gitlab']['dapp_group_id'])
    if len(user_groups) == 1:
        user_group_id = user_groups[0]["id"]
    elif len(user_groups) == 0:
        user_group_id = git_handle.create_group(username, config['gitlab']['dapp_group_id'])
    else:
        _LOGGER.debug(f"Have many groups on gitlab with name: {username}")
        raise ServiceError(f"Have many groups on gitlab with name: {username}")

    dapp_groups = git_handle.get_groups(dapp_name, user_group_id)
    if len(dapp_groups) == 1:
        dapp_group_id = dapp_groups[0]["id"]
    elif len(dapp_groups) == 0:
        dapp_group_id = git_handle.create_group(dapp_name, user_group_id)
    else:
        _LOGGER.debug(f"Have many groups on gitlab with name: {dapp_name}")
        raise ServiceError(f"Have many groups on gitlab with name: {dapp_name}")


    project_smart_contract = git_handle.create_project(smart_contract_project_name, dapp_group_id)
    project_sdk = git_handle.create_project(sdk_project_name, dapp_group_id)

    os.chdir(smart_contract_path)
    cmd = (
            "git init && git add . && git commit -m '"
            + commit_message
            + "' && git remote add origin https://oauth2:" + config['gitlab']["private_token"] + "@gitlab.com/"
            + project_smart_contract["path_with_namespace"]
            + ".git && git push --set-upstream origin master "
    )
    os.system(cmd)

    os.chdir(sdk_path)
    cmd = (
            "git init && git add . && git commit -m '"
            + commit_message
            + "' && git remote add origin https://oauth2:" + config['gitlab']["private_token"] + "@gitlab.com/"
            + project_sdk["path_with_namespace"]
            + ".git && git push --set-upstream origin master "
    )
    os.system(cmd)


    success_message = {
        "data": {
            "user_id": user_info["user_id"],
            "dapp_id": dapp_info["dapp_id"],
            "sdk_project_url": project_sdk["path_with_namespace"]
        }
    }

    _LOGGER.info(success_message)
    broker_client.publish_messages(routing_key=reply_to, message=json.dumps(success_message))
    

