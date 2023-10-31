from logging import exception
import time
from celery.utils.log import get_task_logger
from celery_worker.celery import app
import os
import shutil
from k8s import k8s_operation
import k8s.digitalocean as k8s
from jinja2 import Environment, FileSystemLoader
from settings import config
import const
from utils import file_generator as generate_file_from_template
from network_operation import calNodePort, certificate_operation, channel_operation
from dapp_operation import entitiesLayout, chaincode_operation
from utils import multiple_retry, get_folder_path
from docs import docs
from gitlab import git_handler
from storage import storage_handler
from celery_worker.syn_broker_client import BrokerClientSyn
from exceptions import (
    ThirdPartyRequestError,
    NotSupported,
    ServiceError,
    SchemaError,
    OperationError,
    ChainCodeOperationError,
)
from network.error import NetworkCreateErrorStatus
from dapp.error import ChaincodeOpErrorStatus
import copy

logger = get_task_logger(__name__)

broker_client = BrokerClientSyn(
    username=config["rabbitmq"]["username"],
    password=config["rabbitmq"]["password"],
    host=config["rabbitmq"]["host"],
    port=config["rabbitmq"]["port"],
)

dapp_error_routing_key = "driver.fabric.request.dapp_error"
network_error_routing_key = "driver.fabric.request.network_error"


@app.task
def deploy_fabric(generated_folder, cluster_id, network_info, user_info, reply_to):
    try:
        if os.path.exists(generated_folder):
            shutil.rmtree(generated_folder)

        os.makedirs(generated_folder, exist_ok=True)

        content_config = k8s.get_kubeconfig(
            cluster_id=cluster_id, digital_ocean_token=config["k8s"]["token"]
        )
        kube_config_path = generated_folder + "/k8s_config.yaml"
        file_config = open(kube_config_path, "w")
        file_config.write(content_config)
        file_config.close()

        time_start = time.time()

        while time.time() - time_start <= 3600:
            status = multiple_retry.multiple_retry(
                func=k8s.get_cluster_status,
                kwargs={
                    "cluster_id": cluster_id,
                    "digital_ocean_token": config["k8s"]["token"],
                },
                num_retry=5,
                delay=1
            )

            if status == "running":
                # if True:
                generate_network_file(
                    cluster_id=cluster_id,
                    network_config=network_info,
                    network_folder=generated_folder,
                    user_info=user_info,
                    kube_config_path=kube_config_path,
                    reply_to=reply_to,
                )

                return
            time.sleep(20)

        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_info["network_id"],
                "message": "Failure in Cloud Provider, Please try again later",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

    except (ThirdPartyRequestError, NotSupported) as e:

        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_info["network_id"],
                "message": "Network Error, Please try again later",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def generate_network_file(
    cluster_id, network_config, network_folder, user_info, kube_config_path, reply_to
):
    try:
        username = user_info["username"]
        file_loader = FileSystemLoader(const.BASE_DIR + "/templates/network")
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        env.globals["calPeerNodePort"] = calNodePort.calPeerNodePort
        env.globals["calPeerCaNodePort"] = calNodePort.calPeerCaNodePort
        env.globals["calOrdererNodePort"] = calNodePort.calOrdererNodePort
        env.globals["calOrdererCaNodePort"] = calNodePort.calOrdererCaNodePort

        network_pems = {}

        nodeIp = multiple_retry.multiple_retry(
            func=k8s.get_public_ip,
            kwargs={
                "cluster_id": cluster_id,
                "digital_ocean_token": config["k8s"]["token"],
            },
            num_retry=5,
        )

        delete_all = network_folder + f"/scripts/delete_all.sh"
        delete_all_template = env.get_template("scripts/delete_all_template.jinja2")
        generate_file_from_template.gen_file(
            data={
                "network_name": network_config["name"],
                "network_folder": network_folder,
                "orgs": network_config["blockchain_peer_config"]["organizations"],
                "kube_config_path": kube_config_path,
            },
            dst=delete_all,
            template=delete_all_template,
        )

        fabric_pv = network_folder + f"/k8s/fabric-pv.yaml"
        fabric_pv_template = env.get_template("k8s/fabric_pv_template.jinja2")
        generate_file_from_template.gen_file(
            data={"network_id": network_config["network_id"], "username": username},
            dst=fabric_pv,
            template=fabric_pv_template,
        )
        k8s_operation.apply(file_path=fabric_pv, kube_config_path=kube_config_path)

        fabric_pvc = network_folder + f"/k8s/fabric-pvc.yaml"
        fabric_pvc_template = env.get_template("k8s/fabric_pvc_template.jinja2")
        generate_file_from_template.gen_file(
            data={}, dst=fabric_pvc, template=fabric_pvc_template
        )
        k8s_operation.apply(file_path=fabric_pvc, kube_config_path=kube_config_path)

        orderer_ca_deployment = network_folder + f"/k8s/orderer/ca-deployment.yaml"
        orderer_ca_deployment_template = env.get_template(
            "k8s/ca_orderer_deployment_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={"network_name": network_config["name"], "nodeIp": nodeIp},
            dst=orderer_ca_deployment,
            template=orderer_ca_deployment_template,
        )
        k8s_operation.apply_with_rollout(
            file_path=orderer_ca_deployment,
            name="ca-orderer",
            kube_config_path=kube_config_path,
        )

        orderer_ca_service = network_folder + f"/k8s/orderer/ca-service.yaml"
        orderer_ca_service_template = env.get_template(
            "k8s/ca_orderer_service_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={
                "name": "orderer",
                "network_name": network_config["name"],
                "username": username,
                "nodePort": calNodePort.calOrdererCaNodePort(),
            },
            dst=orderer_ca_service,
            template=orderer_ca_service_template,
        )
        k8s_operation.apply(
            file_path=orderer_ca_service, kube_config_path=kube_config_path
        )

        org_index = 0

        for org in network_config["blockchain_peer_config"]["organizations"]:
            ca_deployment = network_folder + f"/k8s/{org['name']}/ca-deployment.yaml"
            ca_deployment_template = env.get_template(
                "k8s/ca_org_deployment_template.jinja2"
            )
            generate_file_from_template.gen_file(
                data={
                    "org_name": org["name"],
                    "network_name": network_config["name"],
                    "nodeIp": nodeIp,
                },
                dst=ca_deployment,
                template=ca_deployment_template,
            )
            k8s_operation.apply_with_rollout(
                file_path=ca_deployment,
                name=f"ca-org-{org['name']}",
                kube_config_path=kube_config_path,
            )

            temp = copy.deepcopy(org)
            temp["nodePort"] = calNodePort.calPeerCaNodePort(org_index)

            ca_service = network_folder + f"/k8s/{org['name']}/ca-service.yaml"
            ca_service_template = env.get_template("k8s/ca_org_service_template.jinja2")
            generate_file_from_template.gen_file(
                data=temp, dst=ca_service, template=ca_service_template
            )
            k8s_operation.apply(file_path=ca_service, kube_config_path=kube_config_path)

            org_index += 1

        time.sleep(20)

        certificate_operation.gen_certificates_by_network_config(
            network_config=network_config, network_folder=network_folder, nodeIp=nodeIp
        )

        configtx = network_folder + "/config/configtx.yaml"
        configtx_template = env.get_template("config/configtx_template.jinja2")
        generate_file_from_template.gen_file(
            data={
                "network_folder": network_folder,
                "network_name": network_config["name"],
                "orgs": network_config["blockchain_peer_config"]["organizations"],
                "nodeIp": nodeIp,
            },
            dst=configtx,
            template=configtx_template,
        )

        channel_operation.gen_genensis_block(
            configtx_folder_path=f"{network_folder}/config",
            output_folder_path=f"{network_folder}/configtxgen",
            profile_name="TwoOrgsOrdererGenesis",
        )

        channel_operation.gen_channel_tx(
            configtx_folder_path=f"{network_folder}/config",
            output_folder_path=f"{network_folder}/configtxgen",
            profile_name="TwoOrgsChannel",
            channelID=f"{network_config['name']}-appchannel",
        )

        # for org in network_config["blockchain_peer_config"]["organizations"]:
        #     channel_operation.gen_anchorpeer_tx(
        #         configtx_folder_path=f"{network_folder}/config",
        #         output_folder_path=f"{network_folder}/configtxgen",
        #         profile_name="TwoOrgsChannel",
        #         channelID=f"{network_config['name']}-appchannel",
        #         org_name=org["name"],
        #     )

        # fabric_tools = network_folder + f"/k8s/fabric-tools.yaml"
        # fabric_tools_template = env.get_template("k8s/fabric_tools_template.jinja2")
        # generate_file_from_template.gen_file(
        #     data={"network_name": network_config["name"]},
        #     dst=fabric_tools,
        #     template=fabric_tools_template,
        # )

        # k8s_operation.apply(file_path=fabric_tools, kube_config_path=kube_config_path)

        peer_configmap = network_folder + "/k8s/peer_configmap.yaml"
        peer_configmap_template = env.get_template("k8s/peer_configmap_template.jinja2")
        generate_file_from_template.gen_file(
            data={},
            dst=peer_configmap,
            template=peer_configmap_template,
        )
        k8s_operation.apply(peer_configmap, kube_config_path)

        k8s_operation.create_docker_registry_secret(
            username=config["gitlab_pull_dapp_image"]["username"],
            password=config["gitlab_pull_dapp_image"]["password"],
            secret_name="deploy-dapp-secrets",
            kube_config_path=kube_config_path,
        )

        orderer_pem_path = (
            network_folder
            + f"/crypto-config/ordererOrganizations/{network_config['name']}.com/tlsca/tlsca.{network_config['name']}.com-cert.pem"
        )

        with open(orderer_pem_path, "r") as orderer_pem_file:
            orderer_pem = repr(orderer_pem_file.read())[1:-1]
        network_pems["orderer"] = {"orderer_pem": orderer_pem}
        network_pems["organizations"] = {}

        org_index = 0

        peer_file_paths = []
        peer_names = []

        for org in network_config["blockchain_peer_config"]["organizations"]:
            org["nodePort"] = calNodePort.calPeerCaNodePort(org_index)

            peer_pem_path = (
                network_folder
                + f"/crypto-config/peerOrganizations/{org['name']}.{network_config['name']}.com/tlsca/tlsca.{org['name']}.{network_config['name']}.com-cert.pem"
            )
            ca_pem_path = (
                network_folder
                + f"/crypto-config/peerOrganizations/{org['name']}.{network_config['name']}.com/ca/ca.{org['name']}.{network_config['name']}.com-cert.pem"
            )
            with open(peer_pem_path, "r") as peer_pem_file:
                peer_pem = repr(peer_pem_file.read())[1:-1]
            with open(ca_pem_path, "r") as ca_pem_file:
                ca_pem = repr(ca_pem_file.read())[1:-1]

            network_pems["organizations"][org["name"]] = {}
            network_pems["organizations"][org["name"]]["peer_pem"] = peer_pem
            network_pems["organizations"][org["name"]]["ca_pem"] = ca_pem

            # ccp = network_folder + f"/connection-files/ccp-{org['name']}.json"
            # ccp_template_template = env.get_template("config/ccp_template.jinja2")
            # generate_file_from_template.gen_file(
            #     data={
            #         "network_name": network_config["name"],
            #         "org_name": org["name"],
            #         "number_peer": org["number_peer"],
            #         "peer_pem": peer_pem,
            #         "ca_pem": ca_pem,
            #     },
            #     dst=ccp,
            #     template=ccp_template_template,
            # )

            # org_ca_config = (
            #     network_folder + f"/config/{org['name']}/fabric-ca-server-config.yaml"
            # )
            # org_ca_config_template = env.get_template(
            #     "config/fabric_ca_server_config_template.jinja2"
            # )
            # generate_file_from_template.gen_file(
            #     data={"org_name": org["name"], "network_name": network_config["name"]},
            #     dst=org_ca_config,
            #     template=org_ca_config_template,
            # )

            # generate peer deployment
            for peer_index in range(0, org["number_peer"]):

                peer_deployment = (
                    network_folder
                    + f"/k8s/{org['name']}/peer{peer_index}-deployment.yaml"
                )
                peer_deployment_template = env.get_template(
                    "k8s/peer_deployment_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "username": username,
                        "org_name": org["name"],
                        "org_index": org_index,
                        "peer_index": peer_index,
                        "network_name": network_config["name"],
                        "nodeIp": nodeIp,
                    },
                    dst=peer_deployment,
                    template=peer_deployment_template,
                )

                peer_file_paths.append(peer_deployment)
                peer_names.append(f"peer{peer_index}-{org['name']}")
                peer_names.append(f"couchdb{peer_index}-{org['name']}")

                peer_service = (
                    network_folder + f"/k8s/{org['name']}/peer{peer_index}-service.yaml"
                )
                peer_service_template = env.get_template(
                    "k8s/peer_service_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "org_name": org["name"],
                        "peer_index": peer_index,
                        "nodePort": calNodePort.calPeerNodePort(org_index, peer_index),
                    },
                    dst=peer_service,
                    template=peer_service_template,
                )

                k8s_operation.apply(
                    file_path=peer_service, kube_config_path=kube_config_path
                )

            org_index += 1
        k8s_operation.multiple_apply_with_rollout(
            file_paths=peer_file_paths,
            names=peer_names,
            kube_config_path=kube_config_path,
        )

        # create orderer
        orderer_deployment = network_folder + f"/k8s/orderer/orderer-deployment.yaml"
        orderer_deployment_template = env.get_template(
            "k8s/orderer_deployment_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={
                "network_name": network_config["name"],
                "username": username,
            },
            dst=orderer_deployment,
            template=orderer_deployment_template,
        )

        k8s_operation.apply_with_rollout(
            file_path=orderer_deployment,
            name="orderer",
            kube_config_path=kube_config_path,
        )

        orderer_service = network_folder + f"/k8s/orderer/orderer-service.yaml"
        orderer_service_template = env.get_template(
            "k8s/orderer_service_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={}, dst=orderer_service, template=orderer_service_template
        )

        k8s_operation.apply(
            file_path=orderer_service, kube_config_path=kube_config_path
        )

        k8s_operation.create_nginx_ingress(kube_config_path=kube_config_path)

        time.sleep(20)

        multiple_retry.multiple_retry(
            func=channel_operation.create_channel,
            kwargs={
                "network_config": network_config,
                "fabric_cfg_folder": get_folder_path.get_fabric_cfg_folder_path(),
                "nodeIp": nodeIp,
                "crypto_config_folder": f"{network_folder}/crypto-config",
                "org_index": 0,
                "configtxgen_folder": f"{network_folder}/configtxgen",
                "output_folder": f"{network_folder}/output_block",
            },
            num_retry=5,
        )

        time.sleep(20)

        org_index = 0

        for org in network_config["blockchain_peer_config"]["organizations"]:
            for peer_index in range(0, org["number_peer"]):
                # channel_operation.fetch_block(
                #     network_config=network_config,
                #     fabric_cfg_folder=get_folder_path.get_fabric_cfg_folder_path(),
                #     nodeIp=nodeIp,
                #     crypto_config_folder=f"{network_folder}/crypto-config",
                #     block_num=0,
                #     output_folder=f"{network_folder}/output_block",
                #     output_file_name=f"{network_config['name']}-appchannel.block",
                # )

                multiple_retry.multiple_retry(
                    func=channel_operation.join_channel,
                    kwargs={
                        "network_config": network_config,
                        "fabric_cfg_folder": get_folder_path.get_fabric_cfg_folder_path(),
                        "nodeIp": nodeIp,
                        "crypto_config_folder": f"{network_folder}/crypto-config",
                        "org_index": org_index,
                        "peer_index": peer_index,
                        "block_path": f"{network_folder}/output_block/{network_config['name']}-appchannel.block",
                    },
                    num_retry=5,
                )
            org_index += 1

        org_index = 0

        for org in network_config["blockchain_peer_config"]["organizations"]:
            multiple_retry.multiple_retry(
                func=channel_operation.update_ancher_peer,
                kwargs={
                    "network_config": network_config,
                    "fabric_cfg_folder": get_folder_path.get_fabric_cfg_folder_path(),
                    "nodeIp": nodeIp,
                    "crypto_config_folder": f"{network_folder}/crypto-config",
                    "configtxgen_folder": f"{network_folder}/output_block",
                    "org_index": org_index,
                    "peer_index": 0,
                },
                num_retry=5,
            )
            org_index += 1

        explorer_deployment = network_folder + f"/k8s/explorer/explorer-deployment.yaml"
        explorer_deployment_template = env.get_template(
            "k8s/explorer_deployment_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={"network_id": network_config["network_id"]},
            dst=explorer_deployment,
            template=explorer_deployment_template,
        )

        explorer_service = network_folder + f"/k8s/explorer/explorer-service.yaml"
        explorer_service_template = env.get_template(
            "k8s/explorer_service_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={},
            dst=explorer_service,
            template=explorer_service_template,
        )

        explorer_ingress = network_folder + f"/k8s/explorer/explorer_ingress.yaml"
        explorer_ingress_template = env.get_template(
            "k8s/explorer_ingress_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={}, dst=explorer_ingress, template=explorer_ingress_template
        )

        k8s_operation.apply(
            file_path=explorer_service, kube_config_path=kube_config_path
        )

        multiple_retry.multiple_retry(
            func=k8s_operation.apply,
            kwargs={
                "file_path": explorer_ingress,
                "kube_config_path": kube_config_path,
            },
            num_retry=5,
            delay=7,
        )

        explorer_config = network_folder + f"/config/explorer/config.json"
        explorer_config_template = env.get_template(
            "config/explorer_config_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={"network_name": network_config["name"]},
            dst=explorer_config,
            template=explorer_config_template,
        )

        explorer_jwt_config = network_folder + f"/config/explorer/explorerconfig.json"
        explorer_jwt_config_template = env.get_template(
            "config/explorer_jwt_config_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={"secret": network_config["network_id"]},
            dst=explorer_jwt_config,
            template=explorer_jwt_config_template,
        )

        explorer_connection_profile = (
            network_folder + f"/config/explorer/connection-profile/test-network.json"
        )
        explorer_connection_profile_template = env.get_template(
            "config/explorer_connection_profile_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={
                "network_name": network_config["name"],
                "network_folder": network_folder,
                "orgs": network_config["blockchain_peer_config"]["organizations"],
                "kube_config_path": kube_config_path,
                "nodeIp": nodeIp,
            },
            dst=explorer_connection_profile,
            template=explorer_connection_profile_template,
        )

        k8s_operation.multiple_apply_with_rollout(
            file_paths=[explorer_deployment],
            names=["explorer", "explorer-db"],
            kube_config_path=kube_config_path,
            timeout=900,
        )

        explorer_v_chain_ingress = (
            network_folder + f"/k8s/explorer/explorer_v_chain_ingress.yaml"
        )
        explorer_v_chain_ingress_template = env.get_template(
            "k8s/explorer_v_chain_ingress_template.jinja2"
        )

        ingress_ip = k8s_operation.get_ingress_ip(
            "explorer-ingress",
            kube_config_path=kube_config_path,
        )

        generate_file_from_template.gen_file(
            data={
                "network_id": network_config["network_id"],
                "ingress_ip": ingress_ip,
            },
            dst=explorer_v_chain_ingress,
            template=explorer_v_chain_ingress_template,
        )

        k8s_operation.apply(
            file_path=explorer_v_chain_ingress,
            kube_config_path=get_folder_path.get_v_chain_kube_config_path(),
        )

        network_ccp = network_folder + f"/connection-files/ccp.json"
        network_ccp_template = env.get_template("config/network_ccp_template.jinja2")
        generate_file_from_template.gen_file(
            data={
                "config": network_config,
                "pems": network_pems,
                "nodeIp": nodeIp,
                "org_index": 0,
            },
            dst=network_ccp,
            template=network_ccp_template,
        )

        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "network_id": network_config["network_id"],
                "explorer_url": f"explorer.v-chain.vn/explorer/{network_config['network_id']}",
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=success_message)

    except (ThirdPartyRequestError, NotSupported, OperationError) as e:

        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_config["network_id"],
                "message": "Network Error, Please try again later",
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def update_network(
    old_network_config, new_network_config, user_info, update_type, dapps, reply_to
):
    try:
        file_loader = FileSystemLoader(const.BASE_DIR + "/templates/network")
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        env.globals["calPeerNodePort"] = calNodePort.calPeerNodePort
        env.globals["calPeerCaNodePort"] = calNodePort.calPeerCaNodePort
        env.globals["calOrdererNodePort"] = calNodePort.calOrdererNodePort
        env.globals["calOrdererCaNodePort"] = calNodePort.calOrdererCaNodePort

        new_org_definition = False

        nodeIp = multiple_retry.multiple_retry(
            func=k8s.get_public_ip,
            kwargs={
                "cluster_id": old_network_config["cluster_id"],
                "digital_ocean_token": config["k8s"]["token"],
            },
            num_retry=5,
        )

        network_folder = get_folder_path.get_network_folder_path(
            username=user_info["username"], network_id=old_network_config["network_id"]
        )

        kube_config_path = os.path.join(
            get_folder_path.get_kube_config_folder_path(
                username=user_info["username"],
                network_id=old_network_config["network_id"],
            ),
            "k8s_config.yaml",
        )

        temp_network_config = {}

        if update_type == "new_organization":
            old_len = len(old_network_config["blockchain_peer_config"]["organizations"])
            new_orgs = copy.deepcopy(
                new_network_config["blockchain_peer_config"]["organizations"][old_len:]
            )

            org_index = old_len

            for org in new_orgs:
                ca_deployment = (
                    network_folder + f"/k8s/{org['name']}/ca-deployment.yaml"
                )
                ca_deployment_template = env.get_template(
                    "k8s/ca_org_deployment_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "org_name": org["name"],
                        "network_name": old_network_config["name"],
                        "nodeIp": nodeIp,
                    },
                    dst=ca_deployment,
                    template=ca_deployment_template,
                )
                k8s_operation.apply_with_rollout(
                    file_path=ca_deployment,
                    name=f"ca-org-{org['name']}",
                    kube_config_path=kube_config_path,
                )

                temp = copy.deepcopy(org)
                temp["nodePort"] = calNodePort.calPeerCaNodePort(org_index)

                ca_service = network_folder + f"/k8s/{org['name']}/ca-service.yaml"
                ca_service_template = env.get_template(
                    "k8s/ca_org_service_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data=temp, dst=ca_service, template=ca_service_template
                )
                k8s_operation.apply(
                    file_path=ca_service, kube_config_path=kube_config_path
                )

                org_index += 1

            time.sleep(10)

            org_index = old_len
            for org in new_orgs:
                certificate_operation.enroll_org_ca_admin(
                    network_config=new_network_config,
                    network_folder=network_folder,
                    nodeIp=nodeIp,
                    org_index=org_index,
                )

                certificate_operation.create_org_NodeOUS(
                    network_config=new_network_config,
                    network_folder=network_folder,
                    org_index=org_index,
                )

                for peer_index in range(org["number_peer"]):
                    certificate_operation.register_org_entity(
                        network_config=new_network_config,
                        network_folder=network_folder,
                        org_index=org_index,
                        type="peer",
                        name=f"peer{peer_index}",
                        password=f"peer{peer_index}pw",
                    )

                certificate_operation.register_org_entity(
                    network_config=new_network_config,
                    network_folder=network_folder,
                    org_index=org_index,
                    type="client",
                    name=f"user1",
                    password=f"user1pw",
                )

                certificate_operation.register_org_entity(
                    network_config=new_network_config,
                    network_folder=network_folder,
                    org_index=org_index,
                    type="admin",
                    name=f"{org['name']}admin",
                    password=f"{org['name']}adminpw",
                )

                for peer_index in range(org["number_peer"]):
                    certificate_operation.gen_peer_msp(
                        network_config=new_network_config,
                        network_folder=network_folder,
                        nodeIp=nodeIp,
                        org_index=org_index,
                        peer_index=peer_index,
                        hosts=[
                            f"peer{peer_index}.{org['name']}.{old_network_config['name']}.com"
                        ],
                        username=f"peer{peer_index}",
                        password=f"peer{peer_index}pw",
                    )
                    certificate_operation.gen_peer_tls(
                        network_config=new_network_config,
                        network_folder=network_folder,
                        nodeIp=nodeIp,
                        org_index=org_index,
                        peer_index=peer_index,
                        hosts=[
                            f"peer{peer_index}.{org['name']}.{old_network_config['name']}.com",
                            nodeIp,
                            "localhost",
                        ],
                        username=f"peer{peer_index}",
                        password=f"peer{peer_index}pw",
                    )

                certificate_operation.copy_tls_ca_cert_for_org(
                    network_config=new_network_config,
                    network_folder=network_folder,
                    org_index=org_index,
                )

                certificate_operation.gen_user_msp(
                    network_config=new_network_config,
                    network_folder=network_folder,
                    nodeIp=nodeIp,
                    nodePort=calNodePort.calPeerCaNodePort(org_index),
                    org_name=org["name"],
                    org_type="peer",
                    username=f"user1",
                    password=f"user1pw",
                )

                certificate_operation.gen_admin_msp(
                    network_config=new_network_config,
                    network_folder=network_folder,
                    nodeIp=nodeIp,
                    nodePort=calNodePort.calPeerCaNodePort(org_index),
                    org_name=org["name"],
                    org_type="peer",
                    username=f"{org['name']}admin",
                    password=f"{org['name']}adminpw",
                )

                org_index += 1

            org_index = old_len

            peer_file_paths = []
            peer_names = []

            for org in new_orgs:
                org["nodePort"] = calNodePort.calPeerCaNodePort(org_index)

                for peer_index in range(0, org["number_peer"]):

                    peer_deployment = (
                        network_folder
                        + f"/k8s/{org['name']}/peer{peer_index}-deployment.yaml"
                    )
                    peer_deployment_template = env.get_template(
                        "k8s/peer_deployment_template.jinja2"
                    )
                    generate_file_from_template.gen_file(
                        data={
                            "username": user_info["username"],
                            "org_name": org["name"],
                            "org_index": org_index,
                            "peer_index": peer_index,
                            "network_name": old_network_config["name"],
                            "nodeIp": nodeIp,
                        },
                        dst=peer_deployment,
                        template=peer_deployment_template,
                    )

                    peer_file_paths.append(peer_deployment)
                    peer_names.append(f"peer{peer_index}-{org['name']}")
                    peer_names.append(f"couchdb{peer_index}-{org['name']}")

                    peer_service = (
                        network_folder
                        + f"/k8s/{org['name']}/peer{peer_index}-service.yaml"
                    )
                    peer_service_template = env.get_template(
                        "k8s/peer_service_template.jinja2"
                    )
                    generate_file_from_template.gen_file(
                        data={
                            "org_name": org["name"],
                            "peer_index": peer_index,
                            "nodePort": calNodePort.calPeerNodePort(
                                org_index, peer_index
                            ),
                        },
                        dst=peer_service,
                        template=peer_service_template,
                    )

                    k8s_operation.apply(
                        file_path=peer_service, kube_config_path=kube_config_path
                    )

                org_index += 1
            k8s_operation.multiple_apply_with_rollout(
                file_paths=peer_file_paths,
                names=peer_names,
                kube_config_path=kube_config_path,
            )

            fabric_cfg_folder = get_folder_path.get_fabric_cfg_folder_path()
            crypto_config_folder = f"{network_folder}/crypto-config"

            configtx = network_folder + "/config/configtx.yaml"
            configtx_template = env.get_template("config/configtx_template.jinja2")
            generate_file_from_template.gen_file(
                data={
                    "network_folder": network_folder,
                    "network_name": old_network_config["name"],
                    "orgs": new_network_config["blockchain_peer_config"][
                        "organizations"
                    ],
                    "nodeIp": nodeIp,
                },
                dst=configtx,
                template=configtx_template,
            )

            channel_operation.add_new_organizations(
                new_network_config=new_network_config,
                new_org_start_index=old_len,
                fabric_cfg_folder=fabric_cfg_folder,
                nodeIp=nodeIp,
                crypto_config_folder=crypto_config_folder,
                configtxgen_folder=f"{network_folder}/config",
                block_folder=f"{network_folder}/output_block",
            )

            new_org_definition = True

            username = user_info["username"]

            for dapp in dapps:

                dapp_error = dapp["error"] if "error" in dapp else None

                if not dapp_error:

                    cc_folder = get_folder_path.get_dapp_folder_path(
                        username=username,
                        network_id=new_network_config["network_id"],
                        dapp_name=dapp["dapp_name"],
                    )

                    org_index = old_len
                    for org in new_orgs:
                        for peer_index in range(0, org["number_peer"]):
                            multiple_retry.multiple_retry(
                                chaincode_operation.install_chaincode,
                                kwargs={
                                    "network_config": new_network_config,
                                    "dapp_config": dapp,
                                    "fabric_cfg_folder": fabric_cfg_folder,
                                    "package_file_path": f"{cc_folder}/packaging/chaincode.tgz",
                                    "nodeIp": nodeIp,
                                    "crypto_config_folder": crypto_config_folder,
                                    "org_index": org_index,
                                    "peer_index": peer_index,
                                },
                                num_retry=5,
                            )

                        org_index += 1

                    time.sleep(5)

                    package_id = multiple_retry.multiple_retry(
                        chaincode_operation.get_package_id,
                        kwargs={
                            "network_config": new_network_config,
                            "dapp_config": dapp,
                            "fabric_cfg_folder": fabric_cfg_folder,
                            "nodeIp": nodeIp,
                            "crypto_config_folder": crypto_config_folder,
                            "org_index": 0,
                            "peer_index": 0,
                        },
                        num_retry=5,
                    )

                    org_index = old_len
                    for org in new_orgs:
                        multiple_retry.multiple_retry(
                            chaincode_operation.approve_chaincode,
                            kwargs={
                                "network_config": new_network_config,
                                "dapp_config": dapp,
                                "package_id": package_id,
                                "fabric_cfg_folder": fabric_cfg_folder,
                                "nodeIp": nodeIp,
                                "crypto_config_folder": crypto_config_folder,
                                "org_index": org_index,
                            },
                            num_retry=5,
                        )

                        org_index += 1

            temp_network_config["blockchain_peer_config"] = new_network_config[
                "blockchain_peer_config"
            ]

        else:
            raise NotSupported("Update Type not supported")

        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "network_id": old_network_config["network_id"],
                "new_network_config": temp_network_config,
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=success_message)

    except (ThirdPartyRequestError, NotSupported, OperationError) as e:

        if update_type == "new_organization":
            if new_org_definition:
                try:
                    channel_operation.remove_organizations(
                        new_network_config=new_network_config,
                        remove_org_start_index=old_len,
                        fabric_cfg_folder=fabric_cfg_folder,
                        nodeIp=nodeIp,
                        crypto_config_folder=crypto_config_folder,
                        configtxgen_folder=f"{network_folder}/config",
                        block_folder=f"{network_folder}/output_block",
                    )

                except Exception as e:
                    None
            for org in new_orgs:
                ca_deployment = (
                    network_folder + f"/k8s/{org['name']}/ca-deployment.yaml"
                )
                k8s_operation.delete(ca_deployment, kube_config_path)

                ca_service = network_folder + f"/k8s/{org['name']}/ca-service.yaml"
                k8s_operation.delete(ca_service, kube_config_path)

                ca_data_folder = os.path.join(
                    network_folder, "cas", "orgs", org["name"]
                )
                if os.path.exists(ca_data_folder):
                    shutil.rmtree(ca_data_folder)

                crypto_folder = get_folder_path.get_crypto_config_org_folder_path(
                    network_folder, old_network_config["name"], org["name"]
                )
                if os.path.exists(crypto_folder):
                    shutil.rmtree(crypto_folder)

                for peer_index in range(0, org["number_peer"]):
                    peer_deployment = (
                        network_folder
                        + f"/k8s/{org['name']}/peer{peer_index}-deployment.yaml"
                    )
                    k8s_operation.delete(peer_deployment, kube_config_path)

                    peer_service = (
                        network_folder
                        + f"/k8s/{org['name']}/peer{peer_index}-service.yaml"
                    )
                    k8s_operation.delete(peer_service, kube_config_path)

                    peer_data_folder = os.path.join(
                        network_folder, "peerData", f"peer{peer_index}-{org['name']}"
                    )
                    if os.path.exists(peer_data_folder):
                        shutil.rmtree(peer_data_folder)

        temp_network_config = copy.deepcopy(old_network_config)
        temp_network_config["error"] = e.message

        error_message = {
            "network_info": temp_network_config,
            "user_info": user_info,
        }

        broker_client.publish_messages(
            routing_key=network_error_routing_key, message=error_message
        )

        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": old_network_config["network_id"],
                "message": "Network Error, Please try again later",
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def generate_new_remote_peer(
    network_config,
    resource_info,
    user_info,
    resources_folder_id,
    token,
    org_index,
    peer_index,
    host,
    port,
    reply_to,
):
    try:
        file_loader = FileSystemLoader(const.BASE_DIR + "/templates/network")
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        env.globals["calPeerNodePort"] = calNodePort.calPeerNodePort
        env.globals["calPeerCaNodePort"] = calNodePort.calPeerCaNodePort
        env.globals["calOrdererNodePort"] = calNodePort.calOrdererNodePort
        env.globals["calOrdererCaNodePort"] = calNodePort.calOrdererCaNodePort

        nodeIp = multiple_retry.multiple_retry(
            func=k8s.get_public_ip,
            kwargs={
                "cluster_id": network_config["cluster_id"],
                "digital_ocean_token": config["k8s"]["token"],
            },
            num_retry=5,
        )

        network_folder = get_folder_path.get_network_folder_path(
            username=user_info["username"], network_id=network_config["network_id"]
        )

        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]

        certificate_operation.gen_certificates_for_peer(
            network_config=network_config,
            network_folder=network_folder,
            nodeIp=nodeIp,
            org_index=org_index,
            peer_index=peer_index,
            peer_hosts=[host],
        )

        resource_folder = get_folder_path.get_remote_peer_folder_path(
            username=user_info["username"],
            network_id=network_config["network_id"],
            resource_id=resource_info["resource_id"],
        )

        shutil.copytree(
            get_folder_path.get_crypto_config_peer_folder_path(
                base_folder=network_folder,
                network_name=network_config["name"],
                org_name=org_name,
                peer_index=peer_index,
            ),
            get_folder_path.get_crypto_config_peer_folder_path(
                base_folder=resource_folder,
                network_name=network_config["name"],
                org_name=org_name,
                peer_index=peer_index,
            ),
        )

        shutil.copytree(
            get_folder_path.get_crypto_config_org_user_folder_path(
                base_folder=network_folder,
                network_name=network_config["name"],
                org_name=org_name,
                username="Admin",
            ),
            get_folder_path.get_crypto_config_org_user_folder_path(
                base_folder=resource_folder,
                network_name=network_config["name"],
                org_name=org_name,
                username="Admin",
            ),
        )

        shutil.copytree(
            get_folder_path.get_crypto_config_orderer_folder_path(
                base_folder=network_folder,
                network_name=network_config["name"],
                orderer_name="orderer",
            ),
            get_folder_path.get_crypto_config_orderer_folder_path(
                base_folder=resource_folder,
                network_name=network_config["name"],
                orderer_name="orderer",
            ),
        )

        join_channel = resource_folder + f"/scripts/join_channel.sh"
        join_channel_template = env.get_template(
            "scripts/remote_peer_join_channel_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={
                "network_name": network_config["name"],
                "nodeIp": nodeIp,
                "org_name": org_name,
                "peer_index": peer_index,
                "peer_host": host,
                "peer_port": port,
            },
            dst=join_channel,
            template=join_channel_template,
        )

        docker_compose = resource_folder + f"/docker-compose.yaml"
        docker_compose_template = env.get_template(
            "docker/new_peer_docker_compose_template.jinja2"
        )
        generate_file_from_template.gen_file(
            data={
                "network_name": network_config["name"],
                "nodeIp": nodeIp,
                "org_name": org_name,
                "peer_index": peer_index,
                "peer_host": host,
                "peer_port": port,
            },
            dst=docker_compose,
            template=docker_compose_template,
        )
        storage_handler.upload_folder(
            token, resources_folder_id, [user_info["user_id"]], resource_folder
        )

        resources_folder_child_folders = storage_handler.get_folder(
            token, resources_folder_id
        )["child_folders"]

        resource_folder_id = ""
        for child_folder in resources_folder_child_folders:
            if child_folder["name"] == resource_info["resource_id"]:
                resource_folder_id = child_folder["folder_id"]

        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "resource_id": resource_info["resource_id"],
                "resource_folder_id": resource_folder_id,
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=success_message)

    except (ThirdPartyRequestError, NotSupported, OperationError) as e:
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "resource_id": resource_info["resource_id"],
                "message": "Network Error, Please try again later",
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def generate_chaincode_file(
    network_config,
    dapp_config,
    dapp_folder,
    user_info,
    kube_config_path,
    reply_to,
    token,
    dapp_folder_id,
    dapp_version,
    sdk_key,
    error={"code": ChaincodeOpErrorStatus.PRE_ERROR.name, "info": None},
):
    try:
        username = user_info["username"]

        file_loader = FileSystemLoader(const.BASE_DIR + "/templates/dapp")
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        env.globals["calPeerNodePort"] = calNodePort.calPeerNodePort
        env.globals["calPeerCaNodePort"] = calNodePort.calPeerCaNodePort
        env.globals["calOrdererNodePort"] = calNodePort.calOrdererNodePort
        env.globals["calOrdererCaNodePort"] = calNodePort.calOrdererCaNodePort

        nodeIp = multiple_retry.multiple_retry(
            func=k8s.get_public_ip,
            kwargs={
                "cluster_id": network_config["cluster_id"],
                "digital_ocean_token": config["k8s"]["token"],
            },
            num_retry=5,
        )

        layout = entitiesLayout.genLayout(dapp_config)

        layout["doc_layout"]["dapp_id"] = str(dapp_config["dapp_id"])
        layout["doc_layout"]["username"] = username

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.GENFILE_ERROR.value
        ):
            try:

                chaincode_path = dapp_folder + f"/chaincode/chaincode.go"
                chaincode_template = env.get_template(
                    "chaincode/chaincode_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": layout["entities"],
                        "relationships": layout["relationships"],
                        "variables": layout["variables"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=chaincode_path,
                    template=chaincode_template,
                )

                go_mod = dapp_folder + f"/chaincode/go.mod"
                go_mod_template = env.get_template("chaincode/go.jinja2")
                generate_file_from_template.gen_file(
                    data={}, dst=go_mod, template=go_mod_template
                )

                dockerfile = dapp_folder + f"/chaincode/Dockerfile"
                dockerfile_template = env.get_template(
                    "chaincode/dockerfile_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={}, dst=dockerfile, template=dockerfile_template
                )

                gitlab_cid = dapp_folder + f"/chaincode/.gitlab-ci.yml"
                gitlab_cid_template = env.get_template(
                    "chaincode/gitlab_ci_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "dapp_version": dapp_version,
                    },
                    dst=gitlab_cid,
                    template=gitlab_cid_template,
                )

                connection = dapp_folder + f"/packaging/connection.json"
                connection_template = env.get_template(
                    "packaging/connection_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "address": f"{dapp_config['dapp_name']}:7052",
                    },
                    dst=connection,
                    template=connection_template,
                )

                metadata = dapp_folder + f"/packaging/metadata.json"
                metadata_template = env.get_template(
                    "packaging/metadata_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "label": dapp_config["dapp_name"],
                    },
                    dst=metadata,
                    template=metadata_template,
                )

                enroll_admin = dapp_folder + f"/sdk/cli/enrollAdmin.js"
                enroll_admin_template = env.get_template(
                    "sdk/cli/enrollAdmin_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": dapp_config["entities"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=enroll_admin,
                    template=enroll_admin_template,
                )

                register_user = dapp_folder + f"/sdk/cli/registerUser.js"
                register_user_template = env.get_template(
                    "sdk/cli/registerUser_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": dapp_config["entities"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=register_user,
                    template=register_user_template,
                )

                network_export = dapp_folder + f"/sdk/fabric/network.js"
                network_export_template = env.get_template(
                    "sdk/fabric/network_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": layout["entities"],
                        "relationships": layout["relationships"],
                        "variables": layout["variables"],
                        "encryptionType": layout["encryptionType"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=network_export,
                    template=network_export_template,
                )

                encryptionType = layout["encryptionType"]
                encrypt = dapp_folder + f"/sdk/encryption/{encryptionType}.js"
                encrypt_template = env.get_template(
                    f"sdk/encryption/{encryptionType}_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": dapp_config["entities"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=encrypt,
                    template=encrypt_template,
                )

                package_json = dapp_folder + f"/sdk/package.json"
                package_json_template = env.get_template("sdk/package_template.jinja2")
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": dapp_config["entities"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=package_json,
                    template=package_json_template,
                )

                network_folder = get_folder_path.get_network_folder_path(
                    username=username, network_id=network_config["network_id"]
                )

                ccp_path_src = network_folder + "/connection-files/ccp.json"
                ccp_path = dapp_folder + "/sdk/connection-files"
                # ccp_path_dest = ccp_path + "/ccp.json"

                os.makedirs(ccp_path, exist_ok=True)
                # os.system(f"mkdir {ccp_path}")
                shutil.copy(ccp_path_src, ccp_path)
                # os.system(f"cp {ccp_path_src} {ccp_path_dest}")

                # os.system(
                #     f"kubectl --kubeconfig {kube_config_path} exec -i fabric-tools -- /bin/bash /fabric/dapps/{dapp_config['dapp_name']}/scripts/deploy_chaincode.sh"
                # )
            except Exception as e:
                error_code = ChaincodeOpErrorStatus.GENFILE_ERROR.name
                raise ChainCodeOperationError("Fail to generate file", error_code)

        fabric_cfg_folder = get_folder_path.get_fabric_cfg_folder_path()

        network_folder = get_folder_path.get_network_folder_path(
            username=username,
            network_id=network_config["network_id"],
        )
        crypto_config_folder = f"{network_folder}/crypto-config"

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.PACKAGE_ERROR.value
        ):
            try:
                multiple_retry.multiple_retry(
                    chaincode_operation.package_chaincode,
                    kwargs={"packaging_folder": f"{dapp_folder}/packaging"},
                    num_retry=5,
                )
            except OperationError as e:
                error_code = ChaincodeOpErrorStatus.PACKAGE_ERROR.name
                raise ChainCodeOperationError(e.message, error_code)

        dapp_project = None
        dapp_group_id = ""

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.GITLAB_ERROR.value
        ):
            try:
                temp_folder = f"/work/{dapp_config['dapp_id']}"

                shutil.copytree(f"{dapp_folder}/chaincode", temp_folder)

                dapp_groups = git_handler.get_groups(
                    dapp_config["dapp_id"], config["gitlab"]["dapp_group_id"]
                )

                if len(dapp_groups) != 0:
                    for dapp_group in dapp_groups:
                        git_handler.delete_group(dapp_group["id"])
                    time.sleep(30)

                dapp_group_id = git_handler.create_group(
                    dapp_config["dapp_id"], config["gitlab"]["dapp_group_id"]
                )

                dapp_project_name = dapp_config["dapp_id"]

                dapp_project = git_handler.create_project(
                    dapp_project_name, dapp_group_id
                )

                git_handler.push(
                    file_path=temp_folder,
                    project_path=dapp_project["path_with_namespace"],
                    commit_message=f"Version {dapp_version}",
                    private_token=config["gitlab"]["private_token"],
                )

                status = "failed"
                time_start = time.time()
                while time.time() - time_start <= 3600:
                    piplines = git_handler.get_piplines(project_id=dapp_project["id"])
                    if len(piplines) > 0:
                        if (
                            piplines[-1]["status"] == "success"
                            or piplines[-1]["status"] == "failed"
                        ):
                            status = piplines[-1]["status"]
                            break
                    time.sleep(20)

                if status != "success":
                    raise ThirdPartyRequestError("Fail to build Gitlab for Dapp")

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.GITLAB_ERROR.name
                raise ChainCodeOperationError(
                    e.message,
                    error_code,
                )

            finally:
                if os.path.exists(temp_folder):
                    shutil.rmtree(temp_folder)

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.INSTALL_ERROR.value
        ):
            try:
                failed_org_index = 0
                failed_peer_index = 0
                if (
                    ChaincodeOpErrorStatus[error["code"]].value
                    == ChaincodeOpErrorStatus.INSTALL_ERROR.value
                ):
                    failed_org_index = error["info"]["org_index"]
                    failed_peer_index = error["info"]["peer_index"]
                org_index = 0
                for org in network_config["blockchain_peer_config"]["organizations"]:
                    for peer_index in range(0, org["number_peer"]):
                        if org_index >= failed_org_index:
                            # if org_index == 1 and peer_index == 0:
                            #     raise OperationError("test")
                            if peer_index >= failed_peer_index:
                                multiple_retry.multiple_retry(
                                    chaincode_operation.install_chaincode,
                                    kwargs={
                                        "network_config": network_config,
                                        "dapp_config": dapp_config,
                                        "fabric_cfg_folder": fabric_cfg_folder,
                                        "package_file_path": f"{dapp_folder}/packaging/chaincode.tgz",
                                        "nodeIp": nodeIp,
                                        "crypto_config_folder": crypto_config_folder,
                                        "org_index": org_index,
                                        "peer_index": peer_index,
                                    },
                                    num_retry=5,
                                )
                    org_index += 1

                    time.sleep(5)
            except OperationError as e:
                error_code = ChaincodeOpErrorStatus.INSTALL_ERROR.name
                raise ChainCodeOperationError(
                    e.message,
                    error_code,
                    {"org_index": org_index, "peer_index": peer_index},
                )

        package_id = ""

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.DEPLOY_CHAINCODE.value
        ):
            try:
                if not package_id:
                    package_id = chaincode_operation.get_package_id(
                        network_config=network_config,
                        dapp_config=dapp_config,
                        fabric_cfg_folder=fabric_cfg_folder,
                        nodeIp=nodeIp,
                        crypto_config_folder=crypto_config_folder,
                        org_index=0,
                        peer_index=0,
                    )

                if not dapp_project:
                    if not dapp_group_id:
                        dapp_groups = git_handler.get_groups(
                            dapp_config["dapp_id"], config["gitlab"]["dapp_group_id"]
                        )

                        if len(dapp_groups) == 0:
                            dapp_group_id = git_handler.create_group(
                                dapp_config["dapp_id"],
                                config["gitlab"]["dapp_group_id"],
                            )
                        else:
                            dapp_group_id = dapp_groups[0]["id"]

                    projects = git_handler.search_project(
                        dapp_config["dapp_id"], dapp_group_id
                    )

                    dapp_project = projects[0]

                chaincode_deployment = dapp_folder + f"/k8s/chaincode_deployment.yml"
                chaincode_deployment_template = env.get_template(
                    "k8s/chaincode_deployment_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "image": f"registry.gitlab.com/{dapp_project['path_with_namespace']}:{dapp_version}",
                        "dapp_name": dapp_config["dapp_name"],
                        "chaincode_id": package_id,
                    },
                    dst=chaincode_deployment,
                    template=chaincode_deployment_template,
                )

                chaincode_service = dapp_folder + f"/k8s/chaincode_service.yml"
                chaincode_service_template = env.get_template(
                    "k8s/chaincode_service_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=chaincode_service,
                    template=chaincode_service_template,
                )

                k8s_operation.delete(
                    file_path=chaincode_deployment, kube_config_path=kube_config_path
                )

                k8s_operation.apply(
                    file_path=chaincode_service, kube_config_path=kube_config_path
                )

                k8s_operation.apply_with_rollout(
                    file_path=chaincode_deployment,
                    name=dapp_config["dapp_name"],
                    kube_config_path=kube_config_path,
                )

            except (Exception) as e:
                error_code = ChaincodeOpErrorStatus.DEPLOY_CHAINCODE.name
                raise ChainCodeOperationError(
                    "Fail to Deploy Chaincode",
                    error_code,
                )

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.APPROVE_ERROR.value
        ):
            try:
                if not package_id:
                    package_id = chaincode_operation.get_package_id(
                        network_config=network_config,
                        dapp_config=dapp_config,
                        fabric_cfg_folder=fabric_cfg_folder,
                        nodeIp=nodeIp,
                        crypto_config_folder=crypto_config_folder,
                        org_index=0,
                        peer_index=0,
                    )
                failed_org_index = 0
                if (
                    ChaincodeOpErrorStatus[error["code"]].value
                    == ChaincodeOpErrorStatus.APPROVE_ERROR.value
                ):
                    failed_org_index = error["info"]["org_index"]

                org_index = 0
                for org in network_config["blockchain_peer_config"]["organizations"]:
                    if org_index >= failed_org_index:
                        multiple_retry.multiple_retry(
                            chaincode_operation.approve_chaincode,
                            kwargs={
                                "network_config": network_config,
                                "dapp_config": dapp_config,
                                "package_id": package_id,
                                "fabric_cfg_folder": fabric_cfg_folder,
                                "nodeIp": nodeIp,
                                "crypto_config_folder": crypto_config_folder,
                                "org_index": org_index,
                            },
                            num_retry=5,
                        )

                    org_index += 1

                time.sleep(5)

            except OperationError as e:
                error_code = ChaincodeOpErrorStatus.APPROVE_ERROR.name
                raise ChainCodeOperationError(
                    e.message,
                    error_code,
                    {"org_index": org_index},
                )

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.COMMIT_ERROR.value
        ):
            try:
                multiple_retry.multiple_retry(
                    func=chaincode_operation.commit_chaincode_definition,
                    kwargs={
                        "network_config": network_config,
                        "dapp_config": dapp_config,
                        "fabric_cfg_folder": fabric_cfg_folder,
                        "nodeIp": nodeIp,
                        "crypto_config_folder": crypto_config_folder,
                    },
                    num_retry=5,
                )

            except OperationError as e:
                error_code = ChaincodeOpErrorStatus.COMMIT_ERROR.name
                raise ChainCodeOperationError(
                    e.message,
                    error_code,
                )

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.GEN_DOC_ERROR.value
        ):
            try:

                docs.create_doc(layout["doc_layout"])

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.GEN_DOC_ERROR.name
                raise ChainCodeOperationError("Fail to gen doc", error_code)

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.UPLOAD_STORAGE_ERROR.value
        ):
            try:

                dapp_child_folders = storage_handler.get_folder(token, dapp_folder_id)[
                    "child_folders"
                ]

                data_folder_id = ""
                sdk_folder_id = ""
                for child_folder in dapp_child_folders:
                    if child_folder["name"] == "data":
                        data_folder_id = child_folder["folder_id"]
                    if child_folder["name"] == "sdk":
                        sdk_folder_id = child_folder["folder_id"]

                if sdk_folder_id:
                    storage_handler.delete_folder(token, sdk_folder_id)

                if not data_folder_id:
                    data_folder_id = storage_handler.create_folder(
                        token,
                        {
                            "shared": [user_info["user_id"]],
                            "name": "data",
                            "parent_id": dapp_folder_id,
                        },
                    )

                storage_export = dapp_folder + f"/sdk/storage/storage.js"
                storage_export_template = env.get_template(
                    "sdk/storage/storage_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "url": config["v_storage"]["host"],
                        "folder_id": data_folder_id,
                        "sdk_key": sdk_key,
                    },
                    dst=storage_export,
                    template=storage_export_template,
                )

                # dapp_name = dapp_config["dapp_name"]
                sdk_path = dapp_folder + "/sdk"
                # sdk_project_name = dapp_config["dapp_name"] + "sdk"

                storage_handler.upload_folder(
                    token, dapp_folder_id, [user_info["user_id"]], sdk_path
                )

                dapp_child_folders = storage_handler.get_folder(token, dapp_folder_id)[
                    "child_folders"
                ]

                sdk_folder_id = ""
                for child_folder in dapp_child_folders:
                    if child_folder["name"] == "sdk":
                        sdk_folder_id = child_folder["folder_id"]

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.UPLOAD_STORAGE_ERROR.name
                raise ChainCodeOperationError("Fail to upload folder", error_code)

        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_config["dapp_id"],
                "sdk_folder_id": sdk_folder_id,
                "data_folder_id": data_folder_id,
                "sdk_key": sdk_key,
                "dapp_version": dapp_version,
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=success_message)

    except ChainCodeOperationError as e:
        error_message = {
            "dapp_info": {
                "dapp_id": dapp_config["dapp_id"],
                "error": {"code": e.code, "info": e.info},
            },
            "user_info": user_info,
        }

        broker_client.publish_messages(
            routing_key=dapp_error_routing_key, message=error_message
        )

        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_config["network_id"],
                "dapp_id": dapp_config["dapp_id"],
                "message": "Network Error, Please try again later",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

    except (ThirdPartyRequestError, NotSupported, SchemaError) as e:
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_config["network_id"],
                "dapp_id": dapp_config["dapp_id"],
                "message": "Network Error, Please try again later",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def update_chaincode(
    network_config,
    dapp_config,
    dapp_folder,
    user_info,
    kube_config_path,
    reply_to,
    token,
    dapp_folder_id,
    dapp_version,
    sdk_key,
    error={"code": ChaincodeOpErrorStatus.PRE_ERROR.name, "info": None},
):
    try:
        username = user_info["username"]

        file_loader = FileSystemLoader(const.BASE_DIR + "/templates/dapp")
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        env.globals["calPeerNodePort"] = calNodePort.calPeerNodePort
        env.globals["calPeerCaNodePort"] = calNodePort.calPeerCaNodePort
        env.globals["calOrdererNodePort"] = calNodePort.calOrdererNodePort
        env.globals["calOrdererCaNodePort"] = calNodePort.calOrdererCaNodePort

        nodeIp = multiple_retry.multiple_retry(
            func=k8s.get_public_ip,
            kwargs={
                "cluster_id": network_config["cluster_id"],
                "digital_ocean_token": config["k8s"]["token"],
            },
            num_retry=5,
        )

        layout = entitiesLayout.genLayout(dapp_config)

        layout["doc_layout"]["dapp_id"] = str(dapp_config["dapp_id"])
        layout["doc_layout"]["username"] = username

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.GENFILE_ERROR.value
        ):
            try:

                chaincode_path = dapp_folder + f"/chaincode/chaincode.go"
                chaincode_template = env.get_template(
                    "chaincode/chaincode_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": layout["entities"],
                        "relationships": layout["relationships"],
                        "variables": layout["variables"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=chaincode_path,
                    template=chaincode_template,
                )

                gitlab_cid = dapp_folder + f"/chaincode/.gitlab-ci.yml"
                gitlab_cid_template = env.get_template(
                    "chaincode/gitlab_ci_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "dapp_version": dapp_version,
                    },
                    dst=gitlab_cid,
                    template=gitlab_cid_template,
                )

                network_export = dapp_folder + f"/sdk/fabric/network.js"
                network_export_template = env.get_template(
                    "sdk/fabric/network_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": layout["entities"],
                        "relationships": layout["relationships"],
                        "variables": layout["variables"],
                        "encryptionType": layout["encryptionType"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=network_export,
                    template=network_export_template,
                )

                encryptionType = layout["encryptionType"]
                encrypt = dapp_folder + f"/sdk/encryption/{encryptionType}.js"
                encrypt_template = env.get_template(
                    f"sdk/encryption/{encryptionType}_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": dapp_config["entities"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=encrypt,
                    template=encrypt_template,
                )

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.GENFILE_ERROR.name
                raise ChainCodeOperationError("Fail to generate file", error_code)

        fabric_cfg_folder = get_folder_path.get_fabric_cfg_folder_path()

        network_folder = get_folder_path.get_network_folder_path(
            username=username,
            network_id=network_config["network_id"],
        )
        crypto_config_folder = f"{network_folder}/crypto-config"

        dapp_project = None
        dapp_group_id = ""

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.GITLAB_ERROR.value
        ):
            try:
                temp_folder = f"/work/{dapp_config['dapp_id']}"

                os.makedirs(temp_folder, exist_ok=True)

                # shutil.copytree(f"{dapp_folder}/chaincode", temp_folder)

                dapp_groups = git_handler.get_groups(
                    dapp_config["dapp_id"], config["gitlab"]["dapp_group_id"]
                )

                if len(dapp_groups) == 0:
                    dapp_group_id = git_handler.create_group(
                        dapp_config["dapp_id"], config["gitlab"]["dapp_group_id"]
                    )
                else:
                    dapp_group_id = dapp_groups[0]["id"]

                dapp_project_name = dapp_config["dapp_id"]

                projects = git_handler.search_project(dapp_project_name, dapp_group_id)

                if len(projects) == 0:
                    dapp_project = git_handler.create_project(
                        dapp_project_name, dapp_group_id
                    )
                else:
                    dapp_project = projects[0]

                git_handler.pull(
                    file_path=temp_folder,
                    project_path=dapp_project["path_with_namespace"],
                    private_token=config["gitlab"]["private_token"],
                )

                shutil.copy(
                    f"{dapp_folder}/chaincode/chaincode.go",
                    f"{temp_folder}/chaincode.go",
                )
                shutil.copy(
                    f"{dapp_folder}/chaincode/.gitlab-ci.yml",
                    f"{temp_folder}/.gitlab-ci.yml",
                )

                git_handler.push_without_create(
                    file_path=temp_folder,
                    commit_message=f"Version {dapp_version}",
                )

                status = "fail"
                time_start = time.time()
                while time.time() - time_start <= 3600:
                    piplines = git_handler.get_piplines(project_id=dapp_project["id"])
                    if len(piplines) > 0:
                        if (
                            piplines[-1]["status"] == "success"
                            or piplines[-1]["status"] == "failed"
                        ):
                            status = piplines[-1]["status"]
                            break
                    time.sleep(20)

                if status == "fail":
                    raise ThirdPartyRequestError("Fail to build Gitlab for Dapp")

            except (OperationError, ThirdPartyRequestError) as e:
                error_code = ChaincodeOpErrorStatus.GITLAB_ERROR.name
                raise ChainCodeOperationError(
                    e.message,
                    error_code,
                )

            finally:
                if os.path.exists(temp_folder):
                    shutil.rmtree(temp_folder)

        package_id = ""

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.DEPLOY_CHAINCODE.value
        ):
            try:
                if not package_id:
                    package_id = chaincode_operation.get_package_id(
                        network_config=network_config,
                        dapp_config=dapp_config,
                        fabric_cfg_folder=fabric_cfg_folder,
                        nodeIp=nodeIp,
                        crypto_config_folder=crypto_config_folder,
                        org_index=0,
                        peer_index=0,
                    )

                if not dapp_project:
                    if not dapp_group_id:
                        dapp_groups = git_handler.get_groups(
                            dapp_config["dapp_id"], config["gitlab"]["dapp_group_id"]
                        )

                        if len(dapp_groups) == 0:
                            dapp_group_id = git_handler.create_group(
                                dapp_config["dapp_id"],
                                config["gitlab"]["dapp_group_id"],
                            )
                        else:
                            dapp_group_id = dapp_groups[0]["id"]

                    projects = git_handler.search_project(
                        dapp_config["dapp_id"], dapp_group_id
                    )

                    dapp_project = projects[0]

                chaincode_deployment = dapp_folder + f"/k8s/chaincode_deployment.yml"
                chaincode_deployment_template = env.get_template(
                    "k8s/chaincode_deployment_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "image": f"registry.gitlab.com/{dapp_project['path_with_namespace']}:{dapp_version}",
                        "dapp_name": dapp_config["dapp_name"],
                        "chaincode_id": package_id,
                    },
                    dst=chaincode_deployment,
                    template=chaincode_deployment_template,
                )

                chaincode_service = dapp_folder + f"/k8s/chaincode_service.yml"
                chaincode_service_template = env.get_template(
                    "k8s/chaincode_service_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=chaincode_service,
                    template=chaincode_service_template,
                )

                k8s_operation.apply(
                    file_path=chaincode_service, kube_config_path=kube_config_path
                )

                k8s_operation.apply_with_rollout(
                    file_path=chaincode_deployment,
                    name=dapp_config["dapp_name"],
                    kube_config_path=kube_config_path,
                )

            except (Exception) as e:
                error_code = ChaincodeOpErrorStatus.DEPLOY_CHAINCODE.name
                raise ChainCodeOperationError(
                    "Fail to Deploy Chaincode",
                    error_code,
                )

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.GEN_DOC_ERROR.value
        ):
            try:

                docs.create_doc(layout["doc_layout"])

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.GEN_DOC_ERROR.name
                raise ChainCodeOperationError("Fail to gen doc", error_code)

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.UPLOAD_STORAGE_ERROR.value
        ):
            try:

                dapp_child_folders = storage_handler.get_folder(token, dapp_folder_id)[
                    "child_folders"
                ]

                data_folder_id = ""
                sdk_folder_id = ""
                for child_folder in dapp_child_folders:
                    if child_folder["name"] == "data":
                        data_folder_id = child_folder["folder_id"]
                    if child_folder["name"] == "sdk":
                        sdk_folder_id = child_folder["folder_id"]

                if sdk_folder_id:
                    storage_handler.delete_folder(token, sdk_folder_id)

                if not data_folder_id:
                    data_folder_id = storage_handler.create_folder(
                        token,
                        {
                            "shared": [user_info["user_id"]],
                            "name": "data",
                            "parent_id": dapp_folder_id,
                        },
                    )

                storage_export = dapp_folder + f"/sdk/storage/storage.js"
                storage_export_template = env.get_template(
                    "sdk/storage/storage_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "url": config["v_storage"]["host"],
                        "folder_id": data_folder_id,
                        "sdk_key": sdk_key,
                    },
                    dst=storage_export,
                    template=storage_export_template,
                )

                # dapp_name = dapp_config["dapp_name"]
                sdk_path = dapp_folder + "/sdk"
                # sdk_project_name = dapp_config["dapp_name"] + "sdk"

                storage_handler.upload_folder(
                    token, dapp_folder_id, [user_info["user_id"]], sdk_path
                )

                dapp_child_folders = storage_handler.get_folder(token, dapp_folder_id)[
                    "child_folders"
                ]

                sdk_folder_id = ""
                for child_folder in dapp_child_folders:
                    if child_folder["name"] == "sdk":
                        sdk_folder_id = child_folder["folder_id"]

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.UPLOAD_STORAGE_ERROR.name
                raise ChainCodeOperationError("Fail to upload folder", error_code)

        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_config["dapp_id"],
                "sdk_folder_id": sdk_folder_id,
                "data_folder_id": data_folder_id,
                "sdk_key": sdk_key,
                "dapp_version": dapp_version,
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=success_message)

    except ChainCodeOperationError as e:
        error_message = {
            "dapp_info": {
                "dapp_id": dapp_config["dapp_id"],
                "error": {"code": e.code, "info": e.info},
            },
            "user_info": user_info,
        }

        broker_client.publish_messages(
            routing_key=dapp_error_routing_key, message=error_message
        )

        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_config["network_id"],
                "dapp_id": dapp_config["dapp_id"],
                "message": "Network Error, Please try again later",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

    except (ThirdPartyRequestError, NotSupported, SchemaError) as e:
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_config["network_id"],
                "dapp_id": dapp_config["dapp_id"],
                "message": "Network Error, Please try again later",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def rollback_chaincode(
    network_config,
    dapp_config,
    dapp_folder,
    user_info,
    kube_config_path,
    reply_to,
    token,
    dapp_folder_id,
    dapp_version,
    sdk_key,
    error={"code": ChaincodeOpErrorStatus.PRE_ERROR.name, "info": None},
):
    try:
        username = user_info["username"]

        file_loader = FileSystemLoader(const.BASE_DIR + "/templates/dapp")
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        env.globals["calPeerNodePort"] = calNodePort.calPeerNodePort
        env.globals["calPeerCaNodePort"] = calNodePort.calPeerCaNodePort
        env.globals["calOrdererNodePort"] = calNodePort.calOrdererNodePort
        env.globals["calOrdererCaNodePort"] = calNodePort.calOrdererCaNodePort

        nodeIp = multiple_retry.multiple_retry(
            func=k8s.get_public_ip,
            kwargs={
                "cluster_id": network_config["cluster_id"],
                "digital_ocean_token": config["k8s"]["token"],
            },
            num_retry=5,
        )

        layout = entitiesLayout.genLayout(dapp_config)

        layout["doc_layout"]["dapp_id"] = str(dapp_config["dapp_id"])
        layout["doc_layout"]["username"] = username

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.GENFILE_ERROR.value
        ):
            try:
                network_export = dapp_folder + f"/sdk/fabric/network.js"
                network_export_template = env.get_template(
                    "sdk/fabric/network_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": layout["entities"],
                        "relationships": layout["relationships"],
                        "variables": layout["variables"],
                        "encryptionType": layout["encryptionType"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=network_export,
                    template=network_export_template,
                )

                encryptionType = layout["encryptionType"]
                encrypt = dapp_folder + f"/sdk/encryption/{encryptionType}.js"
                encrypt_template = env.get_template(
                    f"sdk/encryption/{encryptionType}_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "network_name": network_config["name"],
                        "orgs": network_config["blockchain_peer_config"][
                            "organizations"
                        ],
                        "entities": dapp_config["entities"],
                        "dapp_name": dapp_config["dapp_name"],
                    },
                    dst=encrypt,
                    template=encrypt_template,
                )

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.GENFILE_ERROR.name
                raise ChainCodeOperationError("Fail to generate file", error_code)

        fabric_cfg_folder = get_folder_path.get_fabric_cfg_folder_path()

        network_folder = get_folder_path.get_network_folder_path(
            username=username,
            network_id=network_config["network_id"],
        )
        crypto_config_folder = f"{network_folder}/crypto-config"

        dapp_project = None
        dapp_group_id = ""

        package_id = ""

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.DEPLOY_CHAINCODE.value
        ):
            try:
                if not package_id:
                    package_id = chaincode_operation.get_package_id(
                        network_config=network_config,
                        dapp_config=dapp_config,
                        fabric_cfg_folder=fabric_cfg_folder,
                        nodeIp=nodeIp,
                        crypto_config_folder=crypto_config_folder,
                        org_index=0,
                        peer_index=0,
                    )

                if not dapp_project:
                    if not dapp_group_id:
                        dapp_groups = git_handler.get_groups(
                            dapp_config["dapp_id"], config["gitlab"]["dapp_group_id"]
                        )

                        if len(dapp_groups) == 0:
                            dapp_group_id = git_handler.create_group(
                                dapp_config["dapp_id"],
                                config["gitlab"]["dapp_group_id"],
                            )
                        else:
                            dapp_group_id = dapp_groups[0]["id"]

                    projects = git_handler.search_project(
                        dapp_config["dapp_id"], dapp_group_id
                    )

                    dapp_project = projects[0]

                chaincode_deployment = dapp_folder + f"/k8s/chaincode_deployment.yml"
                chaincode_deployment_template = env.get_template(
                    "k8s/chaincode_deployment_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "image": f"registry.gitlab.com/{dapp_project['path_with_namespace']}:{dapp_version}",
                        "dapp_name": dapp_config["dapp_name"],
                        "chaincode_id": package_id,
                    },
                    dst=chaincode_deployment,
                    template=chaincode_deployment_template,
                )

                k8s_operation.apply_with_rollout(
                    file_path=chaincode_deployment,
                    name=dapp_config["dapp_name"],
                    kube_config_path=kube_config_path,
                )

            except (Exception) as e:
                error_code = ChaincodeOpErrorStatus.DEPLOY_CHAINCODE.name
                raise ChainCodeOperationError(
                    "Fail to Deploy Chaincode",
                    error_code,
                )

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.GEN_DOC_ERROR.value
        ):
            try:

                docs.create_doc(layout["doc_layout"])

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.GEN_DOC_ERROR.name
                raise ChainCodeOperationError("Fail to gen doc", error_code)

        if (
            ChaincodeOpErrorStatus[error["code"]].value
            <= ChaincodeOpErrorStatus.UPLOAD_STORAGE_ERROR.value
        ):
            try:

                dapp_child_folders = storage_handler.get_folder(token, dapp_folder_id)[
                    "child_folders"
                ]

                data_folder_id = ""
                sdk_folder_id = ""
                for child_folder in dapp_child_folders:
                    if child_folder["name"] == "data":
                        data_folder_id = child_folder["folder_id"]
                    if child_folder["name"] == "sdk":
                        sdk_folder_id = child_folder["folder_id"]

                if sdk_folder_id:
                    storage_handler.delete_folder(token, sdk_folder_id)

                if not data_folder_id:
                    data_folder_id = storage_handler.create_folder(
                        token,
                        {
                            "shared": [user_info["user_id"]],
                            "name": "data",
                            "parent_id": dapp_folder_id,
                        },
                    )

                storage_export = dapp_folder + f"/sdk/storage/storage.js"
                storage_export_template = env.get_template(
                    "sdk/storage/storage_template.jinja2"
                )
                generate_file_from_template.gen_file(
                    data={
                        "url": config["v_storage"]["host"],
                        "folder_id": data_folder_id,
                        "sdk_key": sdk_key,
                    },
                    dst=storage_export,
                    template=storage_export_template,
                )

                # dapp_name = dapp_config["dapp_name"]
                sdk_path = dapp_folder + "/sdk"
                # sdk_project_name = dapp_config["dapp_name"] + "sdk"

                storage_handler.upload_folder(
                    token, dapp_folder_id, [user_info["user_id"]], sdk_path
                )

                dapp_child_folders = storage_handler.get_folder(token, dapp_folder_id)[
                    "child_folders"
                ]

                sdk_folder_id = ""
                for child_folder in dapp_child_folders:
                    if child_folder["name"] == "sdk":
                        sdk_folder_id = child_folder["folder_id"]

            except Exception as e:
                error_code = ChaincodeOpErrorStatus.UPLOAD_STORAGE_ERROR.name
                raise ChainCodeOperationError("Fail to upload folder", error_code)

        success_message = {
            "data": {
                "user_id": user_info["user_id"],
                "dapp_id": dapp_config["dapp_id"],
                "sdk_folder_id": sdk_folder_id,
                "data_folder_id": data_folder_id,
                "sdk_key": sdk_key,
                "dapp_version": dapp_version,
            }
        }

        broker_client.publish_messages(routing_key=reply_to, message=success_message)

    except ChainCodeOperationError as e:
        error_message = {
            "dapp_info": {
                "dapp_id": dapp_config["dapp_id"],
                "error": {"code": e.code, "info": e.info},
            },
            "user_info": user_info,
        }

        broker_client.publish_messages(
            routing_key=dapp_error_routing_key, message=error_message
        )

        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_config["network_id"],
                "dapp_id": dapp_config["dapp_id"],
                "message": "Network Error, Please try again later",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)

    except (ThirdPartyRequestError, NotSupported, SchemaError) as e:
        failure_message = {
            "error": {
                "user_id": user_info["user_id"],
                "network_id": network_config["network_id"],
                "dapp_id": dapp_config["dapp_id"],
                "message": "Network Error, Please try again later",
            }
        }
        broker_client.publish_messages(routing_key=reply_to, message=failure_message)


@app.task
def delete_network_folder(network_info, user_info):
    network_folder = get_folder_path.get_network_folder_path(
        username=user_info["username"], network_id=network_info["network_id"]
    )

    explorer_v_chain_ingress = (
        network_folder + f"/k8s/explorer/explorer_v_chain_ingress.yaml"
    )

    if os.path.exists(explorer_v_chain_ingress):
        k8s_operation.delete(
            file_path=explorer_v_chain_ingress,
            kube_config_path=get_folder_path.get_v_chain_kube_config_path(),
        )

    if os.path.exists(network_folder):
        shutil.rmtree(network_folder)


@app.task
def delete_dapp_folder(network_info, user_info, dapp_info):
    dapp_folder = get_folder_path.get_dapp_folder_path(
        username=user_info["username"],
        network_id=network_info["network_id"],
        dapp_name=dapp_info["dapp_name"],
    )

    kube_config_path = os.path.join(
        get_folder_path.get_kube_config_folder_path(
            username=user_info["username"],
            network_id=network_info["network_id"],
        ),
        "k8s_config.yaml",
    )

    k8s_operation.delete(
        file_path=f"{dapp_folder}/k8s", kube_config_path=kube_config_path
    )

    if os.path.exists(dapp_folder):
        shutil.rmtree(dapp_folder)


@app.task
def delete_dapp_gitlab(dapp_id):
    dapp_groups = git_handler.get_groups(dapp_id, config["gitlab"]["dapp_group_id"])

    if len(dapp_groups) != 0:
        for group in dapp_groups:
            git_handler.delete_group(group["id"])
