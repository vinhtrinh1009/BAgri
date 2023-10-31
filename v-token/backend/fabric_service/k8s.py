import requests
import json
import time

from .logging_config import get_logger
from .exceptions import ThirdPartyRequestError

_LOGGER = get_logger(__name__)

def get_droplet_id(cluster_id, digital_ocean_token):
    url = f"https://api.digitalocean.com/v2/kubernetes/clusters/{cluster_id}/node_pools"
    response = requests.get(
        url,
        headers={"Authorization": digital_ocean_token},
    )
    try:
        droplet_id = json.loads(response.content.decode("utf-8"))["node_pools"][0][
            "nodes"
        ][0]["droplet_id"]
        return droplet_id
    except KeyError:
        raise ThirdPartyRequestError(
            f"Cannot get node pools of cluster {cluster_id} in DigitalOcean"
        )


def get_public_ip(cluster_id, digital_ocean_token):
    droplet_id = get_droplet_id(cluster_id, digital_ocean_token)
    _LOGGER.debug(f"Droplet id {droplet_id}")
    url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}"
    response = requests.get(
        url,
        headers={"Authorization": digital_ocean_token},
    )
    try:
        networks = json.loads(response.content.decode("utf-8"))["droplet"]["networks"][
            "v4"
        ]
        for network in networks:
            if network["type"] == "public":
                public_ip = network["ip_address"]
        return public_ip
    except KeyError:
        raise ThirdPartyRequestError(
            f"Cannot get master node public ip of {cluster_id} in DigitalOcean"
        )
