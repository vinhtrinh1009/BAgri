import os

from jinja2 import Environment, FileSystemLoader

import includes.utils as utils
from constants import BASE_DIR
import subprocess
from kubernetes import client as kubernetes_client
from kubernetes import config as kubernetes_config
import time


def generate(network_folder, consensus, number_peer, network_name, kubeconfig, public_ip, network_id, user_name):
    file_loader = FileSystemLoader(BASE_DIR + "/templates/kubernetes")

    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    kubernetes_file_apply = network_folder + "sawtooth-kubernetes-default.yaml"

    volume_template = env.get_template("persistentVolume.jinja2")
    volume_path = network_folder + "persistentVolume.yaml"
    utils.gen_file(
        data={"username": user_name, "network_id": network_id},
        dst=volume_path,
        template=volume_template,
    )

    volume_claim_template = env.get_template("persistentVolumeClaim.jinja2")
    volume_claim_path = network_folder + "persistentVolumeClaim.yaml"
    utils.gen_file(
        data={},
        dst=volume_claim_path,
        template=volume_claim_template,
    )


    if consensus == "poet" or consensus == "POET":
        addresser_template = env.get_template("sawtooth_poet.jinja2")
        utils.gen_file(
            data={"name": network_name, "number_peer": number_peer,  "public_ip": public_ip},
            dst=kubernetes_file_apply,
            template=addresser_template,
        )
    elif consensus == "pbft" or consensus == "PBFT":

        sawtooth_create_pbft_keys_template = env.get_template("sawtooth_create_pbft_keys.jinja2")
        sawtooth_create_pbft_keys = network_folder + "sawtooth_create_pbft_keys.yaml"
        utils.gen_file(data={"number_peer": number_peer}, dst=sawtooth_create_pbft_keys, template=sawtooth_create_pbft_keys_template)

        os.system(
            "kubectl --kubeconfig=" + kubeconfig + " apply -f " + sawtooth_create_pbft_keys
        )
        time.sleep(3)
        kubernetes_config.load_kube_config(kubeconfig)
        client = kubernetes_client.CoreV1Api()
        time_start = time.time()
        is_success = False
        while time.time() - time_start <= 360 and is_success is False:
            pods = client.list_pod_for_all_namespaces(watch=False)
            for pod in pods.items:
                if str(pod.metadata.name).startswith("pbft-keys"):
                    if str(pod.status.phase) == "Succeeded":
                        keys = client.read_namespaced_pod_log(name=pod.metadata.name, namespace='default')
                        keys_data = keys.splitlines()

                        key_config_map_template = env.get_template("pbft_keys_configmap.jinja2")
                        key_config_map = network_folder + "pbft-keys-configmap.yaml"
                        utils.gen_file(data=keys_data, dst=key_config_map, template=key_config_map_template)
                        is_success = True
                    else:
                        time.sleep(3)
                    break

        sawtooth_template = env.get_template("sawtooth_pbft.jinja2")
        utils.gen_file(
            data={"name": network_name, "number_peer": number_peer, "public_ip": public_ip},
            dst=kubernetes_file_apply,
            template=sawtooth_template,
        )

    else:
        sawtooth_template = env.get_template("sawtooth_poet.jinja2")
        utils.gen_file(
            data={"name": network_name, "number_peer": number_peer,  "public_ip": public_ip},
            dst=kubernetes_file_apply,
            template=sawtooth_template,
        )
    
    deployment_path = network_folder + "deployment.yaml"
    deployment_template = env.get_template("deployment.jinja2")
    utils.gen_file(
        data={"name": network_name, "public_ip": public_ip, "network_id": network_id},
        dst=deployment_path,
        template=deployment_template
    )

    ingress_path = network_folder + "explorer_ingress.yaml"
    ingress_template = env.get_template("explorer_ingress.jinja2")
    utils.gen_file(
        data={"name": network_name, "public_ip": public_ip, "network_id": network_id},
        dst=ingress_path,
        template=ingress_template
    )


