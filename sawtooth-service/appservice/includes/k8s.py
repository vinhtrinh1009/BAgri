import requests
import json
import time

from config.logging_config import get_logger
from exceptions import ThirdPartyRequestError

_LOGGER = get_logger(__name__)

def get_slug_version(digital_ocean_token):
    url = "https://api.digitalocean.com/v2/kubernetes/options"
    response = requests.get(
        url,
        headers={
            "Authorization": digital_ocean_token
        },
    )
    try:
        version = json.loads(response.content.decode("utf-8"))["options"]["versions"][-1]["slug"]
        return version
    except (KeyError, IndexError) as e:
        _LOGGER.debug(f"Cannot get cluster slugversion in digital ocean.")
        raise ThirdPartyRequestError(f"Cannot get cluster slug verion in DigitalOcean")


def create_cluster(name, number_nodes, cpu, ram, digital_ocean_token):
    version = get_slug_version(digital_ocean_token)
    body_request = {
        "name": name,
        "region": "sgp1",
        "version": version,
        "tags": ["sawtooth-network"],
        "node_pools": [
            {
                "size": "s-"
                        + str(cpu)
                        + "vcpu-"
                        + str(ram)
                        + "gb",
                "count": int(number_nodes),
                "name": "sawtooth-pool-" + name,
                "tags": ["sawtooth-pool"],
            }
        ],
    }
    url_k8s = "https://api.digitalocean.com/v2/kubernetes/clusters"
    response = requests.post(
        url_k8s,
        json=body_request,
        headers={
            "Authorization": digital_ocean_token
        },
    )

    response_content = json.loads(response.content.decode("utf-8"))
    try:
        cluster_id = response_content["kubernetes_cluster"]["id"]
        return cluster_id
    except KeyError:
        _LOGGER.debug(f"Cannot create cluster in digital ocean. Response: {response_content}")
        raise ThirdPartyRequestError("Cannot create cluster in digital ocean")


def get_cluster_status(cluster_id, digital_ocean_token):
    url = f"https://api.digitalocean.com/v2/kubernetes/clusters/{cluster_id}"
    response = requests.get(
        url,
        headers={
            "Authorization": digital_ocean_token
        },
    )
    try:
        status = json.loads(response.content.decode("utf-8"))["kubernetes_cluster"]["status"]["state"]
        return status
    except KeyError:
        raise ThirdPartyRequestError(f"Cannot get status of cluster {cluster_id} in DigitalOcean")

def get_droplet_id(cluster_id, digital_ocean_token):
    url = f"https://api.digitalocean.com/v2/kubernetes/clusters/{cluster_id}/node_pools"
    response = requests.get(
        url,
        headers={
            "Authorization": digital_ocean_token
        },
    )
    try:
        droplet_id = json.loads(response.content.decode("utf-8"))["node_pools"][0]["nodes"][0]["droplet_id"]
        return droplet_id
    except KeyError:
        raise ThirdPartyRequestError(f"Cannot get node pools of cluster {cluster_id} in DigitalOcean")

def get_public_ip(cluster_id, digital_ocean_token):
    droplet_id = get_droplet_id(cluster_id, digital_ocean_token)
    _LOGGER.debug(f"Droplet id {droplet_id}")
    url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}"
    response = requests.get(
        url,
        headers={
            "Authorization": digital_ocean_token
        },
    )
    try:
        networks = json.loads(response.content.decode("utf-8"))["droplet"]["networks"]["v4"]
        for network in networks:
            if network["type"] == "public":
                public_ip = network["ip_address"]
        return public_ip
    except KeyError:
        raise ThirdPartyRequestError(f"Cannot get master node public ip of {cluster_id} in DigitalOcean")

def delete_cluster(cluster_id, digital_ocean_token):
    url_k8s = "https://api.digitalocean.com/v2/kubernetes/clusters"
    url_get_status = url_k8s + "/" + str(cluster_id) + "/destroy_with_associated_resources/dangerous"
    response = requests.delete(
        url_get_status,
        headers={
            "Authorization": digital_ocean_token
        },
    )
    # _LOGGER.debug(response)
    if response.status_code != 204:
        raise ThirdPartyRequestError(f"Cannot delete k8s cluster {cluster_id} in DigitalOcean")


def get_kubeconfig(cluster_id, digital_ocean_token):
    url_get_config = "https://api.digitalocean.com/v2/kubernetes/clusters" + "/" + str(cluster_id) + "/kubeconfig"
    time_start = time.time()
    response_get = requests.get(
        url_get_config,
        headers={
            "Authorization": digital_ocean_token
        },
    )
    while response_get.status_code != 200:
        time.sleep(10)
        response_get = requests.get(
            url_get_config,
            headers={
                "Authorization": digital_ocean_token
            },
        )
        if time.time() - time_start >= 60:
            raise ThirdPartyRequestError(f"Cannot retrieve kubeconfig of cluster {cluster_id}")
    return response_get.content.decode("utf-8")
