from network_operation import calNodePort
import json
import subprocess
import os
import shutil

from exceptions import (
    OperationError,
)


def go_mod_vender(chaincode_source_path, dest_folder):
    try:
        if os.path.exists(dest_folder):
            shutil.rmtree(dest_folder)

        # os.makedirs(dest_folder, exist_ok=True)

        shutil.copytree(chaincode_source_path, dest_folder)

        env = dict(
            **os.environ,
            GO111MODULE="on",
        )
        cmd = []
        cmd.append("go")
        cmd.append("mod")
        cmd.append("vendor")

        subprocess.run(cmd, check=True, env=env, cwd=dest_folder)
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to go vendor")


def package_chaincode(
    packaging_folder,
):
    try:
        code_tar = "code.tar.gz"
        chaincode_tar = "chaincode.tgz"

        if os.path.exists(os.path.join(packaging_folder, code_tar)):
            os.remove(os.path.join(packaging_folder, code_tar))

        if os.path.exists(os.path.join(packaging_folder, chaincode_tar)):
            os.remove(os.path.join(packaging_folder, chaincode_tar))


        env = dict(
            **os.environ,
        )

        cmd = []

        cmd.append("tar")
        cmd.append("cfz")
        cmd.append(code_tar)
        cmd.append("connection.json")

        subprocess.run(cmd, check=True, env=env, cwd=packaging_folder)

        cmd = []

        cmd.append("tar")
        cmd.append("cfz")
        cmd.append(chaincode_tar)
        cmd.append(code_tar)
        cmd.append("metadata.json")

        subprocess.run(cmd, check=True, env=env, cwd=packaging_folder)

    except Exception as e:
        print(e)
        raise OperationError(f"Fail to package Chaincode")


def install_chaincode(
    network_config,
    dapp_config,
    fabric_cfg_folder,
    package_file_path,
    nodeIp,
    crypto_config_folder,
    org_index,
    peer_index,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calNodePort.calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_folder,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_folder,
            "peerOrganizations",
            f"{org_name}.{network_name}.com",
        )

        peer_tls_rootcert_file = os.path.join(
            org_crypto_config_folder,
            "peers",
            f"peer{peer_index}.{org_name}.{network_name}.com",
            "tls",
            "ca.crt",
        )

        peer_mspconfigpath = os.path.join(
            org_crypto_config_folder,
            "users",
            f"Admin@{org_name}.{network_name}.com",
            "msp",
        )

        env = dict(
            **os.environ,
            CORE_PEER_TLS_ENABLED="true",
            ORDERER_CA=orderer_ca,
            ORDERER_URL=orderer_url,
            CORE_PEER_ADDRESSAUTODETECT="false",
            CHANNEL_NAME=channel_name,
            FABRIC_CFG_PATH=fabric_cfg_folder,
            CORE_PEER_LOCALMSPID=f"{org_name.capitalize()}MSP",
            CORE_PEER_TLS_ROOTCERT_FILE=peer_tls_rootcert_file,
            CORE_PEER_MSPCONFIGPATH=peer_mspconfigpath,
            CORE_PEER_ADDRESS=f"{nodeIp}:{calNodePort.calPeerNodePort(org_index, peer_index)}",
        )

        cmd = []

        cmd.append("peer")
        cmd.append("lifecycle")
        cmd.append("chaincode")

        cmd.append("install")
        cmd.append(package_file_path)

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(
            f"Fail to install chaincode for peer {peer_index} of Organization of index {org_index}"
        )


def get_package_id(
    network_config,
    dapp_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    org_index,
    peer_index,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calNodePort.calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_folder,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_folder,
            "peerOrganizations",
            f"{org_name}.{network_name}.com",
        )

        peer_tls_rootcert_file = os.path.join(
            org_crypto_config_folder,
            "peers",
            f"peer{peer_index}.{org_name}.{network_name}.com",
            "tls",
            "ca.crt",
        )

        peer_mspconfigpath = os.path.join(
            org_crypto_config_folder,
            "users",
            f"Admin@{org_name}.{network_name}.com",
            "msp",
        )

        env = dict(
            **os.environ,
            CORE_PEER_TLS_ENABLED="true",
            ORDERER_CA=orderer_ca,
            ORDERER_URL=orderer_url,
            CORE_PEER_ADDRESSAUTODETECT="false",
            CHANNEL_NAME=channel_name,
            FABRIC_CFG_PATH=fabric_cfg_folder,
            CORE_PEER_LOCALMSPID=f"{org_name.capitalize()}MSP",
            CORE_PEER_TLS_ROOTCERT_FILE=peer_tls_rootcert_file,
            CORE_PEER_MSPCONFIGPATH=peer_mspconfigpath,
            CORE_PEER_ADDRESS=f"{nodeIp}:{calNodePort.calPeerNodePort(org_index, peer_index)}",
        )

        cmd = []

        cmd.append("peer")
        cmd.append("lifecycle")
        cmd.append("chaincode")

        cmd.append("queryinstalled")

        result = subprocess.run(
            cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).stdout.decode("utf-8")

        start = result.find(
            f"{dapp_config['dapp_name']}:"
        )
        end = result.find(
            f", Label: {dapp_config['dapp_name']}"
        )

        if start < 0 or end < 0:
            raise OperationError(
                f"Fail to querry chaincode for peer {peer_index} of Organization of index {org_index}"
            )

        return result[start:end]
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to get package ID")


def approve_chaincode(
    network_config,
    dapp_config,
    package_id,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    org_index,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calNodePort.calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_folder,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_folder,
            "peerOrganizations",
            f"{org_name}.{network_name}.com",
        )

        peer_tls_rootcert_file = os.path.join(
            org_crypto_config_folder,
            "peers",
            f"peer0.{org_name}.{network_name}.com",
            "tls",
            "ca.crt",
        )

        peer_mspconfigpath = os.path.join(
            org_crypto_config_folder,
            "users",
            f"Admin@{org_name}.{network_name}.com",
            "msp",
        )

        env = dict(
            **os.environ,
            CORE_PEER_TLS_ENABLED="true",
            ORDERER_CA=orderer_ca,
            ORDERER_URL=orderer_url,
            CORE_PEER_ADDRESSAUTODETECT="false",
            CHANNEL_NAME=channel_name,
            FABRIC_CFG_PATH=fabric_cfg_folder,
            CORE_PEER_LOCALMSPID=f"{org_name.capitalize()}MSP",
            CORE_PEER_TLS_ROOTCERT_FILE=peer_tls_rootcert_file,
            CORE_PEER_MSPCONFIGPATH=peer_mspconfigpath,
            CORE_PEER_ADDRESS=f"{nodeIp}:{calNodePort.calPeerNodePort(org_index, 0)}",
        )

        cmd = []

        cmd.append("peer")
        cmd.append("lifecycle")
        cmd.append("chaincode")

        cmd.append("approveformyorg")

        cmd.append("-o")
        cmd.append(orderer_url)

        cmd.append("--tls")

        cmd.append("--cafile")
        cmd.append(orderer_ca)

        cmd.append("--channelID")
        cmd.append(channel_name)

        cmd.append("--name")
        cmd.append(dapp_config["dapp_name"])

        cmd.append("--version")
        cmd.append("1")

        cmd.append("--sequence")
        cmd.append("1")

        cmd.append("--package-id")
        cmd.append(package_id)

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(
            f"Fail to Approve chaincode for Organization of index {org_index}"
        )


def check_commit_readiness(
    network_config,
    dapp_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    org_index,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calNodePort.calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_folder,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_folder,
            "peerOrganizations",
            f"{org_name}.{network_name}.com",
        )

        peer_tls_rootcert_file = os.path.join(
            org_crypto_config_folder,
            "peers",
            f"peer0.{org_name}.{network_name}.com",
            "tls",
            "ca.crt",
        )

        peer_mspconfigpath = os.path.join(
            org_crypto_config_folder,
            "users",
            f"Admin@{org_name}.{network_name}.com",
            "msp",
        )

        env = dict(
            **os.environ,
            CORE_PEER_TLS_ENABLED="true",
            ORDERER_CA=orderer_ca,
            ORDERER_URL=orderer_url,
            CORE_PEER_ADDRESSAUTODETECT="false",
            CHANNEL_NAME=channel_name,
            FABRIC_CFG_PATH=fabric_cfg_folder,
            CORE_PEER_LOCALMSPID=f"{org_name.capitalize()}MSP",
            CORE_PEER_TLS_ROOTCERT_FILE=peer_tls_rootcert_file,
            CORE_PEER_MSPCONFIGPATH=peer_mspconfigpath,
            CORE_PEER_ADDRESS=f"{nodeIp}:{calNodePort.calPeerNodePort(org_index, 0)}",
        )

        cmd = []

        cmd.append("peer")
        cmd.append("lifecycle")
        cmd.append("chaincode")

        cmd.append("checkcommitreadiness")

        # cmd.append("-o")
        # cmd.append(orderer_url)

        cmd.append("--tls")

        cmd.append("--cafile")
        cmd.append(orderer_ca)

        cmd.append("--channelID")
        cmd.append(channel_name)

        cmd.append("--name")
        cmd.append(dapp_config["dapp_name"])

        cmd.append("--version")
        cmd.append(str(dapp_config["dapp_version"]))

        cmd.append("--sequence")
        cmd.append(str(dapp_config["dapp_version"]))

        cmd.append("--output")
        cmd.append("json")

        return json.loads(
            subprocess.run(
                cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).stdout.decode("utf-8")
        )
    except Exception as e:
        print(e)
        raise OperationError(
            f"Fail to Approve chaincode for Organization of index {org_index}"
        )


def commit_chaincode_definition(
    network_config,
    dapp_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][0]["name"]
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calNodePort.calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_folder,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_folder,
            "peerOrganizations",
            f"{org_name}.{network_name}.com",
        )

        peer_tls_rootcert_file = os.path.join(
            org_crypto_config_folder,
            "peers",
            f"peer0.{org_name}.{network_name}.com",
            "tls",
            "ca.crt",
        )

        peer_mspconfigpath = os.path.join(
            org_crypto_config_folder,
            "users",
            f"Admin@{org_name}.{network_name}.com",
            "msp",
        )

        env = dict(
            **os.environ,
            CORE_PEER_TLS_ENABLED="true",
            ORDERER_CA=orderer_ca,
            ORDERER_URL=orderer_url,
            CORE_PEER_ADDRESSAUTODETECT="false",
            CHANNEL_NAME=channel_name,
            FABRIC_CFG_PATH=fabric_cfg_folder,
            CORE_PEER_LOCALMSPID=f"{org_name.capitalize()}MSP",
            CORE_PEER_TLS_ROOTCERT_FILE=peer_tls_rootcert_file,
            CORE_PEER_MSPCONFIGPATH=peer_mspconfigpath,
            CORE_PEER_ADDRESS=f"{nodeIp}:{calNodePort.calPeerNodePort(0, 0)}",
        )

        cmd = []

        cmd.append("peer")
        cmd.append("lifecycle")
        cmd.append("chaincode")

        cmd.append("commit")

        cmd.append("-o")
        cmd.append(orderer_url)

        cmd.append("--tls")

        cmd.append("--cafile")
        cmd.append(orderer_ca)

        cmd.append("--channelID")
        cmd.append(channel_name)

        cmd.append("--name")
        cmd.append(dapp_config["dapp_name"])

        cmd.append("--version")
        cmd.append(str(dapp_config["dapp_version"]))

        cmd.append("--sequence")
        cmd.append(str(dapp_config["dapp_version"]))

        org_index = 0

        for org in network_config["blockchain_peer_config"]["organizations"]:
            cmd.append("--peerAddresses")
            cmd.append(f"{nodeIp}:{calNodePort.calPeerNodePort(org_index, 0)}")

            org_crypto_config_folder = os.path.join(
                crypto_config_folder,
                "peerOrganizations",
                f"{org['name']}.{network_name}.com",
            )

            peer_tls_rootcert_file = os.path.join(
                org_crypto_config_folder,
                "peers",
                f"peer0.{org['name']}.{network_name}.com",
                "tls",
                "ca.crt",
            )

            cmd.append("--tlsRootCertFiles")
            cmd.append(peer_tls_rootcert_file)

            org_index += 1

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to Commit Chaincode Definition")
