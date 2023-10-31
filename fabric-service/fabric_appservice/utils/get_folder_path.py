import os
import const


def get_fabric_cfg_folder_path():
    return os.path.join("/fabric-samples", "config")


def get_network_folder_path(username, network_id):
    return os.path.join(
        const.BASE_DIR,
        "projects",
        username,
        network_id,
    )


def get_v_chain_kube_config_path():
    return os.path.join(
        const.BASE_DIR,
        "k8s",
        "v-chain-prod-kubeconfig.yaml",
    )


def get_kube_config_folder_path(username, network_id):
    return get_network_folder_path(username, network_id)


def get_remote_peer_folder_path(username, network_id, resource_id):
    return os.path.join(
        get_network_folder_path(username, network_id),
        "resources",
        resource_id,
    )


def get_crypto_config_org_folder_path(base_folder, network_name, org_name):
    return os.path.join(
        base_folder,
        "crypto-config",
        "peerOrganizations",
        f"{org_name}.{network_name}.com",
    )


def get_crypto_config_peer_folder_path(base_folder, network_name, org_name, peer_index):
    return os.path.join(
        get_crypto_config_org_folder_path(base_folder, network_name, org_name),
        "peers",
        f"peer{peer_index}.{org_name}.{network_name}.com",
    )


def get_crypto_config_org_user_folder_path(
    base_folder, network_name, org_name, username
):
    return os.path.join(
        get_crypto_config_org_folder_path(base_folder, network_name, org_name),
        "users",
        f"{username.capitalize()}@{org_name}.{network_name}.com",
    )


def get_crypto_config_org_orderer_folder_path(base_folder, network_name):
    return os.path.join(
        base_folder,
        "crypto-config",
        "ordererOrganizations",
        f"{network_name}.com",
    )


def get_crypto_config_orderer_folder_path(base_folder, network_name, orderer_name):
    return os.path.join(
        get_crypto_config_org_orderer_folder_path(base_folder, network_name),
        "orderers",
        f"{orderer_name}.{network_name}.com",
    )


def get_crypto_config_org_orderer_user_folder_path(base_folder, network_name, username):
    return os.path.join(
        get_crypto_config_org_orderer_folder_path(base_folder, network_name),
        "users",
        f"{username.capitalize()}@{network_name}.com",
    )


def get_dapp_folder_path(username, network_id, dapp_name):
    return os.path.join(
        get_network_folder_path(username, network_id),
        "dapps",
        dapp_name,
    )
