from __future__ import absolute_import, unicode_literals
from math import pi
import os
import time
import asyncio
import json

from urllib3 import Retry

from kombu import Connection, Queue, Exchange, Consumer, Producer, exceptions
from .celery import app
import includes.git_handler as git_handle
from settings import config
from celery.utils.log import get_task_logger
from exceptions import StorageServiceRequestError, ThirdPartyRequestError, NotSupported, ServiceError, OperationError
from includes import k8s
from worker.syn_broker_client import BrokerClientSyn

import constants
from kubernetes import client as kubernetes_client
from kubernetes import config as kubernetes_config
from generator import sawtooth_generator, vchain_ingress_gen
from includes.storage_handler import delete_folder, upload_folder
from config.logging_config import get_logger
from operation import k8s_operation, gitlab_operation
from network.error import NetworkError
from includes import multi_retry
from constants import BASE_DIR
# _LOGGER = get_task_logger(__name__)

_LOGGER = get_logger(__name__)

# db = Database(host=config["database"]["host"],
#               port=config["database"]["port"],
#               username=config["database"]["username"],
#               password=config["database"]["password"],
#               dbname=config["database"]["db_name"])

broker_client = BrokerClientSyn(username=config["rabbitmq"]["username"],
                                password=config["rabbitmq"]["password"],
                                host=config["rabbitmq"]["host"],
                                port=config["rabbitmq"]["port"])

network_error_routing_key = "driver.sawtooth.request.network_error"


@app.task
def deploy_sawtooth(cluster_id, network_info, user_info, reply_to):
    network_folder = os.path.join(constants.BASE_DIR,
                                  "network/{}/{}/".format(user_info["username"], network_info["network_id"]))

    volume_folder = os.path.join(constants.BASE_DIR,
                                  "volume/{}/{}/".format(user_info["username"], network_info["network_id"]))
    
    if not os.path.exists(network_folder):
        os.makedirs(network_folder)

    if not os.path.exists(volume_folder):
        os.makedirs(volume_folder)

    try:
        content_config = k8s.get_kubeconfig(cluster_id=cluster_id, digital_ocean_token=config['k8s']['token'])
        k8s_config_path = network_folder + "k8s_config.yaml"
        file_config = open(k8s_config_path, "w")
        file_config.write(content_config)
        file_config.close()

        time_start = time.time()

        while time.time() - time_start <= 3600:
            status = k8s.get_cluster_status(cluster_id=cluster_id, digital_ocean_token=config['k8s']['token'])
            if status == "running":
                public_ip = k8s.get_public_ip(cluster_id=cluster_id, digital_ocean_token=config["k8s"]["token"])
                sawtooth_generator.generate(network_folder=network_folder,
                                            consensus=network_info["consensus"],
                                            number_peer=network_info["blockchain_peer_config"]["number_peer"],
                                            network_name=network_info["name"],
                                            kubeconfig=k8s_config_path,
                                            public_ip=public_ip,
                                            network_id=network_info["network_id"],
                                            user_name=user_info["username"])
                number_peer=network_info["blockchain_peer_config"]["number_peer"]
                temp_names = []

                for x in range(number_peer-1):
                    peer_name = network_info["name"] + "-" + str(x)
                    temp_names.append(peer_name)

                volume_path = network_folder + "persistentVolume.yaml"

                volume_claim_path = network_folder + "persistentVolumeClaim.yaml"

                k8s_operation.apply(file_path=volume_path, kube_config_path=k8s_config_path)

                k8s_operation.apply(file_path=volume_claim_path, kube_config_path=k8s_config_path)
                

                if network_info["consensus"].lower() == "poet":

                    # os.system(
                    #     "kubectl --kubeconfig=" + k8s_config_path + " apply -f " + network_folder +
                    #     "/sawtooth-kubernetes-default.yaml"
                    # )
                    file_path = network_folder + "sawtooth-kubernetes-default.yaml"

                    k8s_operation.apply(file_path=file_path, kube_config_path=k8s_config_path)
                    
                    k8s_operation.multiple_rollout(names=temp_names, kube_config_path=k8s_config_path)
                    
                elif network_info["consensus"].lower() == "pbft":
                    # os.system(
                    #     "kubectl --kubeconfig=" + k8s_config_path + " apply -f " + network_folder +
                    #     "pbft-keys-configmap.yaml"
                    # )
                    file_path = network_folder + "/pbft-keys-configmap.yaml"

                    k8s_operation.apply(file_path=file_path, kube_config_path=k8s_config_path)
                    # os.system(
                    #     "kubectl --kubeconfig=" + k8s_config_path + " apply -f " + network_folder +
                    #     "/sawtooth-kubernetes-default.yaml"
                    # )
                    file_path2 = network_folder + "sawtooth-kubernetes-default.yaml"
                    k8s_operation.apply(file_path=file_path2, kube_config_path=k8s_config_path)

                    k8s_operation.multiple_rollout(names=temp_names, kube_config_path=k8s_config_path)
                    
                    

                else:
                    raise NotSupported(f"Do not support the consensus type: {network_info['consensus']}")
                
                # os.system(
                #         "kubectl --kubeconfig=" + k8s_config_path + " apply -f " + network_folder +
                #         "/deployment.yaml"
                #     )
                
                # success_message = {
                #     "data": {
                #         "user_id": user_info["user_id"],
                #         "network_id": network_info["network_id"],
                #     }
                # }
                # broker_client.publish_messages(routing_key=reply_to, message=success_message)
                deploy_explorer.delay(k8s_config_path, network_info, user_info, network_folder, public_ip,reply_to)
                return public_ip
            time.sleep(20)
        error_message = {
            "network_info": {
                "network_id": network_info["network_id"],
                "error": NetworkError.CLUSTER_CREATE_TIMEOUT.name,
            },
            "user_info": user_info,
        }

        broker_client.publish_messages(
            routing_key=network_error_routing_key, message=error_message
        )


        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_info["network_id"],
                "message": "Cannot create cluster after 3600s"
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

    except (ThirdPartyRequestError, NotSupported, OperationError) as e:
        error_message = {
            "network_info": {
                "network_id": network_info["network_id"],
                "error": NetworkError.CLUSTER_CREATE_ERROR.name,
            },
            "user_info": user_info,
        }

        broker_client.publish_messages(
            routing_key=network_error_routing_key, message=error_message
        )
        
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_info["network_id"],
                "message": e.message
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

@app.task
def deploy_explorer(k8s_config_path, network_info, user_info, network_folder, public_ip,reply_to):
    # os.system(
    #      "kubectl --kubeconfig=" + k8s_config_path + " apply -f " + network_folder +
    #      "/deployment.yaml"
    # )
    try: 
        # deploy backend explorer
        file_path = network_folder + "/deployment.yaml"
        temp_name = network_info["name"] + "-explorer"

        k8s_operation.apply(file_path=file_path, kube_config_path=k8s_config_path)

        k8s_operation.rollout(name=temp_name, kube_config_path=k8s_config_path)

        # create ingress
        ingress_path = network_folder + "explorer_ingress.yaml"
        
        k8s_operation.create_nginx_ingress(kube_config_path=k8s_config_path)
        
        multi_retry.multiple_retry(
            func=k8s_operation.apply,
            kwargs={
                "file_path": ingress_path,
                "kube_config_path": k8s_config_path,
            },
            num_retry=5,
            delay=7,
        )
        ingress_ip = multi_retry.multiple_retry(
            func=k8s_operation.get_ingress_ip,
            kwargs={
                "ingress_name": "explorer-ingress",
                "kube_config_path": k8s_config_path,
            },
            num_retry=5,
            delay=7,
        )
        # gen file deploy ingress to v-chain
        vchain_ingress_gen.generate(network_folder, ingress_ip, network_info["network_id"])
        vchain_ingress_path = network_folder + "explorer_vchain_ingress.yaml"

        vchain_pod_config_path = os.path.join(
            BASE_DIR,
            "k8s",
            "v-chain-prod-kubeconfig.yaml",
        )

        k8s_operation.apply(file_path=vchain_ingress_path, kube_config_path=vchain_pod_config_path)
                    
        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "network_id": network_info["network_id"],
                "explorer_url": f"explorer.v-chain.vn/explorer/{network_info['network_id']}"
            }
        }
        _LOGGER.debug(success_message, reply_to)

        broker_client.publish_messages(routing_key=reply_to, message=success_message)
    
    except (ThirdPartyRequestError, NotSupported, OperationError) as e:
        error_message = {
            "network_info": {
                "network_id": network_info["network_id"],
                "error": NetworkError.CLUSTER_CREATE_ERROR.name,
            },
            "user_info": user_info,
        }

        broker_client.publish_messages(
            routing_key=network_error_routing_key, message=error_message
        )
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_info["network_id"],
                "message": e.message
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def git_push_without_create(
    user_id, dapp_id, username, dapp_name, dapp_version, 
    sdk_path, processor_path, commit_message, number_peer, 
    network_id, sdk_folder_id, data_folder_id, sdk_key,
    reply_to):
    try:    
        cmd = (
                "cd "
                + sdk_path
                + " && git add . && git commit -m '"
                + commit_message
                + "' && git push"
        )
        os.system(cmd)
        # gitlab_operation.push_without_create(file_path=sdk_path, commit_message=commit_message)
        cmd = (
                "cd "
                + processor_path
                + " && git add . && git commit -m '"
                + commit_message
                + "' && git push"
        )
        os.system(cmd)
        # gitlab_operation.push_without_create(file_path=processor_path, commit_message=commit_message)
        # time.sleep(30)
        # check_status.delay(module_name)
        status = "fail"
        time_start = time.time()
        user_groups = git_handle.get_groups(username, config['gitlab']['dapp_group_id'])
        dapp_groups = git_handle.get_groups(dapp_name, user_groups[0]["id"])
        dapps = git_handle.search_project(dapp_name + "processor", dapp_groups[0]["id"])
        while time.time() - time_start <= 3600:
            piplines = git_handle.get_piplines(project_id=dapps[0]["id"])
            if len(piplines) > 0:
                if piplines[0]["status"] == "success" or piplines[0]["status"] == "failed":
                    status = piplines[0]["status"]
                    break
            time.sleep(20)
        if status == "success":
            temp_names=[]
            k8s_config_path = os.path.join(constants.BASE_DIR,
                                    "network/{}/{}/k8s_config.yaml".format(username,
                                                                            network_id))
            for x in range(number_peer-1):
                    temp_name = dapp_name +"processorapp" +"-" + str(x)
                    temp_names.append(temp_name)
            k8s_operation.multiple_rollout(names=temp_names, kube_config_path=k8s_config_path)
            success_message = {
                "data": {
                    "user_id": user_id,
                    "dapp_id": dapp_id, 
                    "dapp_version": dapp_version,
                    "sdk_folder_id": sdk_folder_id,
                    "data_folder_id": data_folder_id,
                    "sdk_key": sdk_key
                }
            }
            _LOGGER.info(success_message)
            broker_client.publish_messages(routing_key=reply_to, message=success_message)
        else:
            failure_message = {
                "error": {
                    "user_id": user_id,
                    "dapp_id": dapp_id,
                    "message": f"Fail to get pipline dapp {dapp_id} ",
                }
            }
            broker_client.publish_messages(routing_key=reply_to, message=failure_message)
    except Exception as e:
        failure_message = {
            "error": {
                "user_id": user_id,
                "dapp_id": dapp_id,
                "dapp_version": dapp_version-1,
                "message": f"Fail to push dapp {dapp_id} ",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def git_push(
        user_id,
        dapp_id,
        username,
        user_group_id,
        dapp_name,
        network_id,
        sdk_path,
        processor_path,
        sdk_project_name,
        processor_project_name,
        commit_message,
        number_peer,
        sdk_folder_id,
        data_folder_id,
        sdk_key,
        reply_to
):
    try:    
        dapp_groups = git_handle.get_groups(dapp_name, user_group_id)
        if len(dapp_groups) == 1:
            dapp_group_id = dapp_groups[0]["id"]
        elif len(dapp_groups) == 0:
            dapp_group_id = git_handle.create_group(dapp_name, user_group_id)
        else:
            _LOGGER.debug(f"Have many groups on gitlab with name: {dapp_name}")
            raise ServiceError(f"Have many groups on gitlab with name: {dapp_name}")

        k8s_config_path = os.path.join(constants.BASE_DIR,
                                    "network/{}/{}/k8s_config.yaml".format(username,
                                                                            network_id))
        with open(k8s_config_path) as f:
            k8s_config_content = f.read()
            print("===k8s_config_content===")
            print(k8s_config_content)

        git_handle.create_variable(name="k8s_config", value=k8s_config_content, group_id=dapp_group_id)

        # project_sdk = git_handle.create_project(sdk_project_name, dapp_group_id)
        project_processor = git_handle.create_project(processor_project_name, dapp_group_id)
        # cmd = (
        #         "cd "
        #         + sdk_path
        #         + "&& git init && git add . && git commit -m '"
        #         + commit_message
        #         + "' && git remote add origin https://oauth2:" + config['gitlab']["private_token"] + "@gitlab.com/"
        #         + project_sdk["path_with_namespace"]
        #         + ".git && git push --set-upstream origin master "
        # )
        # os.system(cmd)
        # _LOGGER.debug(project_sdk["path_with_namespace"])
        # gitlab_operation.push(file_path=sdk_path, project_path=project_sdk["path_with_namespace"],commit_message=commit_message, private_token=config['gitlab']["private_token"])
        cmd2 = (
                "cd "
                + processor_path
                + "&& git init && git add . && git commit -m '"
                + commit_message
                + "' && git remote add origin https://oauth2:" + config['gitlab']["private_token"] + "@gitlab.com/"
                + project_processor["path_with_namespace"]
                + ".git && git push --set-upstream origin master "
        )
        os.system(cmd2)
        # gitlab_operation.push(file_path=processor_path, project_path=project_processor["path_with_namespace"],commit_message=commit_message, private_token=config['gitlab']["private_token"])

        status = "fail"
        time_start = time.time()
        while time.time() - time_start <= 4800:
            piplines = git_handle.get_piplines(project_id=project_processor["id"])
            if len(piplines) > 0:
                if piplines[-1]["status"] == "success" or piplines[-1]["status"] == "failed":
                    status = piplines[-1]["status"]
                    break
            time.sleep(20)
       
        if status == "success":
            _LOGGER.debug(status)
            temp_names=[]
            for x in range(number_peer-1):
                temp_name = dapp_name +"processorapp" +"-" + str(x)
                temp_names.append(temp_name)
            _LOGGER.debug(temp_names)
            k8s_operation.multiple_rollout(names=temp_names, kube_config_path=k8s_config_path)
            success_message = {
                    "data": {
                        "user_id": user_id,
                        "dapp_id": dapp_id,
                        "sdk_folder_id": sdk_folder_id,
                        "data_folder_id": data_folder_id,
                        "sdk_key": sdk_key
                    }
                }
            _LOGGER.info(success_message)
            broker_client.publish_messages(routing_key=reply_to, message=success_message)
        else:
            failure_message = {
                "error": {
                    "user_id": user_id,
                    "dapp_id": dapp_id,
                    "message": f"Fail to get pipline dapp {dapp_id} ",
                }
            }
            broker_client.publish_messages(routing_key=reply_to, message=failure_message)
    except Exception as e:
        failure_message = {
            "error": {
                "user_id": user_id,
                "dapp_id": dapp_id,
                "message": f"Fail to push dapp {dapp_id} ",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task(time_limit=1800)
def check_status(dapp_name, k8s_config_path):
    while 1:
        res = elastic.get_app_user_by_name(module_name)
        try:
            app_ = res["hits"]["hits"][0]["_source"]
            id_ = res["hits"]["hits"][0]["_id"]
        except:
            app_ = {}
            id_ = None
        if app_ != {}:
            # private_token = "2DwFAdURFACk1RS-HPp6"
            flag_check_update = False
            status_temp = app_["status"]
            if status_temp.upper() == "running".upper():
                break
            # check kubernutes
            flag_update_kurbernutes = False
            kubernetes_config.load_kube_config(k8s_config_path)
            v1 = kubernetes_client.CoreV1Api()
            ret = v1.list_pod_for_all_namespaces(watch=False)
            for j in ret.items:
                if str(j.metadata.name).startswith(app_["name"] + "restapiapp-"):
                    app_["status"] = j.status.phase
                    flag_update_kurbernutes = True
                    break
            if not flag_update_kurbernutes:
                # check gitlab
                try:
                    rest_api_id = app_["idGitlab"]["rest_api_id"]
                    proccessor_api_id = app_["idGitlab"]["proccessor_id"]
                    url_rest_api_status = (
                            "https://gitlab.com/api/v4/projects/"
                            + str(rest_api_id)
                            + "/pipelines?private_token="
                            + cfg['gitlab']['private_token']
                    )
                    response_rest_api = requests.get(url_rest_api_status)
                    response_rest_api = json.loads(response_rest_api.text)
                    rest_api_status = response_rest_api[0]["status"]

                    url_processor = (
                            "https://gitlab.com/api/v4/projects/"
                            + str(proccessor_api_id)
                            + "/pipelines?private_token="
                            + cfg['gitlab']['private_token']
                    )
                    response_processor = requests.get(url_processor)
                    response_processor = json.loads(response_processor.text)
                    processor_status = response_processor[0]["status"]
                except:
                    rest_api_status = "false"
                    processor_status = "false"

                if (
                        (processor_status == "success") & (rest_api_status == "success")
                ) or ((processor_status == "running") & (rest_api_status == "running")):
                    app_["status"] = "deploying"

            if app_["status"] != status_temp:
                flag_check_update = True
            if flag_check_update:
                body_update = {"doc": app_}
                status_update = False
                while not status_update:
                    res = elastic.update_app_user(id_, body_update)
                    if res["result"] == "updated":
                        print(app_["status"])
                        status_update = True
                if app_["status"].upper() == "running".upper():
                    break

        time.sleep(10)


@app.task
def task_upload_sdk(token, owner, sdk_folder_id, folder_path, 
    data_folder_id, processor_path, user_info, dapp_info, dapp_folder_id, 
    number_peer, reply_to):
    try:    
        upload_folder(token, sdk_folder_id, [owner], folder_path)
        task_upload_procesor.delay(
            sdk_folder_id, data_folder_id, processor_path, user_info, 
            dapp_info, dapp_folder_id, folder_path, number_peer, reply_to)
    except Exception as e:
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_info["dapp_id"],
                "dapp_folder_id": sdk_folder_id,
                "message": "Fail to upload dapp folder",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

@app.task
def task_upload_procesor(sdk_folder_id, data_folder_id, 
    folder_path, user_info, dapp_info, dapp_folder_id, sdk_path, number_peer, reply_to):
    # result = upload_folder(token, owner, parent_id, folder_path)
    # _LOGGER.debug({result['status']})
    try:    
        sdk_project_name = dapp_info["dapp_name"] + "sdk"
        processor_project_name = dapp_info["dapp_name"] + "processor"

        if (dapp_info["dapp_version"] == 1 and "rollback" not in dapp_info) :
            git_push.delay(user_id=user_info["user_id"],
                            dapp_id=dapp_info["dapp_id"],  
                            username = user_info["username"], 
                            user_group_id=user_info["user_group_id"],
                            dapp_name=dapp_info["dapp_name"],
                            network_id=dapp_info["network_id"],
                            sdk_path=sdk_path,
                            processor_path=folder_path,
                            sdk_project_name=sdk_project_name,
                            processor_project_name=processor_project_name,
                            commit_message="create dapp",
                            number_peer=number_peer,
                            sdk_folder_id=sdk_folder_id,
                            data_folder_id=data_folder_id,
                            sdk_key=dapp_info["sdk_key"],
                            reply_to=reply_to)
        else:
            git_push_without_create.delay(
                user_info["user_id"],
                dapp_info["dapp_id"],
                user_info["username"], 
                dapp_info["dapp_name"],
                dapp_info["dapp_version"],
                sdk_path, folder_path, 
                "update version " +  str(dapp_info["dapp_version"]),
                number_peer,
                dapp_info["network_id"],
                sdk_folder_id,
                data_folder_id,
                dapp_info["sdk_key"],
                reply_to
                )
    except Exception as e:
        _LOGGER.debug(e)
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_info["dapp_id"],
                "dapp_folder_id": dapp_folder_id,
                "message": "Fail to upload dapp folder",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

@app.task
def task_delete_folder(token, dapp_folder_id, user_info, dapp_info, reply_to):
    try:
        if dapp_folder_id != -1:
            delete_folder(token, dapp_folder_id)
            _LOGGER.debug(f"Deleted dapp with dapp_id")
        success_message = {
                "data": {
                    "user_id": user_info["user_id"],
                    "dapp_id": dapp_info["dapp_id"],
                    "dapp_folder_id": dapp_folder_id
                }
        }
        broker_client.publish_messages(routing_key=reply_to, message=success_message)
    except Exception as e:
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_info["dapp_id"],
                "message": "Fail to delete dapp folder",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def task_delete_folder_network(token, folder_id, user_info, info, dapp_infos, deleted_dapps,reply_to):
    try:    
        delete_folder(token, folder_id)
        _LOGGER.debug(f"Deleted network with id:")
        success_message = {
                "data": {
                    "user_id": user_info["user_id"],
                    "network_id": info["network_id"]
                }
        }
        broker_client.publish_messages(routing_key=reply_to, message=success_message)
    except Exception as e:
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": info["network_id"],
                "list_dapps": dapp_infos,
                "deleted_dapps": deleted_dapps,
                "message": "Fail to delete network folder",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

@app.task
def task_upload_resources(token, user_info, parent_id, folder_path, resource_info,reply_to):
    try:
        
        upload_folder(token, parent_id, [user_info["user_id"]], folder_path)
        success_message = {
                "data": {
                    "user_id": user_info["user_id"],
                    "resource_id": resource_info["resource_id"],
                    "resource_folder_id": parent_id
                }
            }
        broker_client.publish_messages(routing_key=reply_to, message=success_message)
    except Exception as e:
        failure_message = {
            "error": {
                    "user_id": user_info["user_id"],
                    "resource_id": resource_info["resource_id"],
                    "message": "Fail to upload resource folder",
                }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)
    
@app.task
def task_update_sdk(token, owner, old_folder_id, new_folder_id,folder_path, data_folder_id, processor_path, user_info, dapp_info, dapp_folder_id, number_peer, reply_to):
    try:
        if old_folder_id != -1:
            delete_folder(token, old_folder_id)
        upload_folder(token, new_folder_id, [owner], folder_path)
        task_upload_procesor.delay(new_folder_id, data_folder_id, processor_path, user_info, dapp_info, dapp_folder_id, folder_path, number_peer, reply_to)
    except StorageServiceRequestError as e:
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_info["dapp_id"],
                "dapp_version": dapp_info["dapp_version"],
                "message": "Fail to upload dapp folder",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)