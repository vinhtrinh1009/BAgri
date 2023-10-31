import os

from jinja2 import Environment, FileSystemLoader

import includes.utils as utils
from constants import BASE_DIR
from kubernetes import client as kubernetes_client
from kubernetes import config as kubernetes_config


def generate(network_folder, ingress_ip, network_id):
    file_loader = FileSystemLoader(BASE_DIR + "/templates/kubernetes")

    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    ingress_path = network_folder + "explorer_vchain_ingress.yaml"
    ingress_template = env.get_template("explorer_vchain_ingress.jinja2")
    utils.gen_file(
        data={"ingress_ip":ingress_ip, "network_id":network_id},
        dst=ingress_path,
        template=ingress_template
    )