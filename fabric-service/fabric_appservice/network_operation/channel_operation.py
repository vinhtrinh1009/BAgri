from network_operation import calNodePort
import subprocess
import os, copy
import shutil
from utils import multiple_retry

from exceptions import (
    OperationError,
)


def gen_genensis_block(configtx_folder_path, output_folder_path, profile_name):
    try:
        env = dict(
            **os.environ,
            FABRIC_CFG_PATH=f"{configtx_folder_path}",
        )

        cmd = []

        cmd.append("configtxgen")

        cmd.append("-profile")
        cmd.append(profile_name)

        cmd.append("-channelID")
        cmd.append("system-channel")

        cmd.append("-outputBlock")
        cmd.append(f"{output_folder_path}/genesis.block")

        subprocess.run(cmd, check=True, env=env)

    except Exception as e:
        raise OperationError("Fail to generate genesis block")


def gen_channel_tx(configtx_folder_path, output_folder_path, profile_name, channelID):
    try:
        env = dict(
            **os.environ,
            FABRIC_CFG_PATH=f"{configtx_folder_path}",
        )

        cmd = []

        cmd.append("configtxgen")

        cmd.append("-profile")
        cmd.append(f"{profile_name}")

        cmd.append("-channelID")
        cmd.append(f"{channelID}")

        cmd.append("-outputCreateChannelTx")
        cmd.append(f"{output_folder_path}/{channelID}.tx")

        subprocess.run(cmd, check=True, env=env)

    except Exception as e:
        raise OperationError("Fail to generate channel transaction")


def gen_anchorpeer_tx(
    configtx_folder_path, output_folder_path, profile_name, channelID, org_name
):
    try:
        env = dict(
            **os.environ,
            FABRIC_CFG_PATH=f"{configtx_folder_path}",
        )

        cmd = []

        cmd.append("configtxgen")

        cmd.append("-profile")
        cmd.append(f"{profile_name}")

        cmd.append("-channelID")
        cmd.append(f"{channelID}")

        cmd.append("-outputAnchorPeersUpdate")
        cmd.append(f"{output_folder_path}/{org_name.capitalize()}MSPanchors.tx")

        cmd.append("-asOrg")
        cmd.append(f"{org_name.capitalize()}MSP")

        subprocess.run(cmd, check=True, env=env)

    except Exception as e:
        raise OperationError(f"Fail to generate anchorpeer transaction for {org_name}")


def create_channel(
    network_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    org_index,
    configtxgen_folder,
    output_folder,
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

        os.makedirs(
            output_folder,
            exist_ok=True,
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
        cmd.append("channel")
        cmd.append("create")

        cmd.append("-o")
        cmd.append(orderer_url)

        cmd.append("-c")
        cmd.append(channel_name)

        cmd.append("-f")
        cmd.append(f"{configtxgen_folder}/{channel_name}.tx")

        cmd.append("--outputBlock")
        cmd.append(f"{output_folder}/{channel_name}.block")

        cmd.append("--tls")

        cmd.append("--cafile")
        cmd.append(orderer_ca)

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to create Channel")


def fetch_block(
    network_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    block_num,
    output_folder,
    output_file_name,
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

        os.makedirs(
            output_folder,
            exist_ok=True,
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
        cmd.append("channel")
        cmd.append("fetch")

        cmd.append(str(block_num))
        cmd.append(f"{output_folder}/{output_file_name}")

        cmd.append("-o")
        cmd.append(orderer_url)

        cmd.append("-c")
        cmd.append(channel_name)

        cmd.append("--tls")

        cmd.append("--cafile")
        cmd.append(orderer_ca)

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to fetch Block")


def join_channel(
    network_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    block_path,
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
        cmd.append("channel")
        cmd.append("join")

        cmd.append("-b")
        cmd.append(block_path)

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(
            f"Fail to join peer {peer_index} of Organization of index {org_index} into Channel"
        )


def submit_update(
    network_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    file_path,
    org_index,
):
    try:
        peer_index = 0
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
        cmd.append("channel")
        cmd.append("update")

        cmd.append("-f")
        cmd.append(file_path)

        cmd.append("-o")
        cmd.append(orderer_url)

        cmd.append("-c")
        cmd.append(channel_name)

        cmd.append("--tls")

        cmd.append("--cafile")
        cmd.append(orderer_ca)

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to submit update")


def update_ancher_peer(
    network_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    configtxgen_folder,
    org_index,
    peer_index,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        channel_name = f"{network_name}-appchannel"

        config_pb_file_name = "config_block.pb"
        config_js_file_name = "config_block.json"

        isolated_config_js_file_name = f"{org_name}config_block.json"

        config_folder_path = os.path.join(configtxgen_folder, org_name)

        os.makedirs(config_folder_path, exist_ok=True)

        fetch_block(
            network_config=network_config,
            fabric_cfg_folder=fabric_cfg_folder,
            nodeIp=nodeIp,
            crypto_config_folder=crypto_config_folder,
            block_num="config",
            output_folder=config_folder_path,
            output_file_name=config_pb_file_name,
        )

        env = dict(
            **os.environ,
        )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_decode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, config_pb_file_name))
        cmd.append("--type")
        cmd.append("common.Block")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, config_js_file_name))
        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                "jq .data.data[0].payload.data.config {} >'{}'".format(
                    os.path.join(config_folder_path, config_js_file_name),
                    os.path.join(config_folder_path, isolated_config_js_file_name),
                )
            ],
            shell=True,
            check=True,
        )

        modified_config_js_file_name = f"{org_name}modified_config.json"

        str = 'jq \'.channel_group.groups.Application.groups.\'{}\'.values += {{"AnchorPeers":{{"mod_policy": "Admins","value":{{"anchor_peers": [{{"host": "\'{}\'","port": \'{}\'}}]}},"version": "0"}}}}\' {} > {}'.format(
            f"{org_name.capitalize()}MSP",
            nodeIp,
            calNodePort.calPeerNodePort(org_index, peer_index),
            os.path.join(config_folder_path, isolated_config_js_file_name),
            os.path.join(config_folder_path, modified_config_js_file_name),
        )

        subprocess.run(
            [str],
            shell=True,
            check=True,
        )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, isolated_config_js_file_name))
        cmd.append("--type")
        cmd.append("common.Config")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "original_config.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, modified_config_js_file_name))
        cmd.append("--type")
        cmd.append("common.Config")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "modified_config.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("compute_update")
        cmd.append("--channel_id")
        cmd.append(channel_name)
        cmd.append("--original")
        cmd.append(os.path.join(config_folder_path, "original_config.pb"))
        cmd.append("--updated")
        cmd.append(os.path.join(config_folder_path, "modified_config.pb"))
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "config_update.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_decode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "config_update.pb"))
        cmd.append("--type")
        cmd.append("common.ConfigUpdate")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "config_update.json"))
        subprocess.run(cmd, check=True, env=env)

        str = 'echo \'{{"payload":{{"header":{{"channel_header":{{"channel_id":"\'{}\'", "type":2}}}},"data":{{"config_update":\'$(cat {})\'}}}}}}\' | jq . > {}'.format(
            channel_name,
            os.path.join(config_folder_path, "config_update.json"),
            os.path.join(config_folder_path, "config_update_in_envelope.json"),
        )
        subprocess.run(
            [str],
            shell=True,
            check=True,
        )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "config_update_in_envelope.json"))
        cmd.append("--type")
        cmd.append("common.Envelope")
        cmd.append("--output")
        cmd.append(
            os.path.join(config_folder_path, f"{org_name.capitalize()}MSPanchors.tx")
        )
        subprocess.run(cmd, check=True, env=env)

        submit_update(
            network_config=network_config,
            fabric_cfg_folder=fabric_cfg_folder,
            nodeIp=nodeIp,
            crypto_config_folder=crypto_config_folder,
            file_path=os.path.join(
                config_folder_path, f"{org_name.capitalize()}MSPanchors.tx"
            ),
            org_index=org_index,
        )

        # cmd = []

        # cmd.append("peer")
        # cmd.append("channel")
        # cmd.append("update")

        # cmd.append("-f")
        # cmd.append(
        #     os.path.join(config_folder_path, f"{org_name.capitalize()}MSPanchors.tx")
        # )

        # cmd.append("-o")
        # cmd.append(orderer_url)

        # cmd.append("-c")
        # cmd.append(channel_name)

        # cmd.append("--tls")

        # cmd.append("--cafile")
        # cmd.append(orderer_ca)

        # subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(
            f"Fail to update peer {peer_index} as Ancher Peer of Organization of index {org_index}"
        )


def sign_configtx(
    network_config,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    file_path,
    org_index,
):
    try:
        peer_index = 0
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
        cmd.append("channel")
        cmd.append("signconfigtx")

        cmd.append("-f")
        cmd.append(file_path)

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to sign from Organization of index {org_index}")


def add_new_organizations(
    new_network_config,
    new_org_start_index,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    configtxgen_folder,
    block_folder,
):
    try:
        network_name = new_network_config["name"]
        channel_name = f"{network_name}-appchannel"

        new_orgs = copy.deepcopy(
            new_network_config["blockchain_peer_config"]["organizations"][
                new_org_start_index:
            ]
        )

        config_folder_path = os.path.join(
            block_folder, f"add_org_from{new_org_start_index}"
        )

        config_pb_file_name = "config_block.pb"
        config_js_file_name = "config_block.json"

        os.makedirs(config_folder_path, exist_ok=True)

        env = dict(
            **os.environ,
        )

        fetch_block(
            network_config=new_network_config,
            fabric_cfg_folder=fabric_cfg_folder,
            nodeIp=nodeIp,
            crypto_config_folder=crypto_config_folder,
            block_num="config",
            output_folder=config_folder_path,
            output_file_name=config_pb_file_name,
        )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_decode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, config_pb_file_name))
        cmd.append("--type")
        cmd.append("common.Block")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, config_js_file_name))
        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                "jq .data.data[0].payload.data.config {} >'{}'".format(
                    os.path.join(config_folder_path, config_js_file_name),
                    os.path.join(config_folder_path, "config.json"),
                )
            ],
            shell=True,
            check=True,
        )

        shutil.copyfile(
            os.path.join(config_folder_path, "config.json"),
            os.path.join(config_folder_path, "temp_config.json"),
        )

        env = dict(
            **os.environ,
            FABRIC_CFG_PATH=f"{configtxgen_folder}",
        )

        for org in new_orgs:
            str = "configtxgen -printOrg {} > {}".format(
                f"{org['name'].capitalize()}MSP",
                os.path.join(config_folder_path, f"{org['name']}.json"),
            )
            subprocess.run(
                [str],
                shell=True,
                env=env,
                check=True,
            )

            str = 'jq -s \'.[0] * {{"channel_group":{{"groups":{{"Application":{{"groups": {{"{}":.[1]}}}}}}}}}}\' {} {} > {}'.format(
                f"{org['name'].capitalize()}MSP",
                os.path.join(config_folder_path, "temp_config.json"),
                os.path.join(config_folder_path, f"{org['name']}.json"),
                os.path.join(config_folder_path, "modified_config.json"),
            )

            subprocess.run(
                [str],
                shell=True,
                check=True,
            )

            shutil.copyfile(
                os.path.join(config_folder_path, "modified_config.json"),
                os.path.join(config_folder_path, "temp_config.json"),
            )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "config.json"))
        cmd.append("--type")
        cmd.append("common.Config")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "config.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "modified_config.json"))
        cmd.append("--type")
        cmd.append("common.Config")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "modified_config.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("compute_update")
        cmd.append("--channel_id")
        cmd.append(channel_name)
        cmd.append("--original")
        cmd.append(os.path.join(config_folder_path, "config.pb"))
        cmd.append("--updated")
        cmd.append(os.path.join(config_folder_path, "modified_config.pb"))
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "config_update.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_decode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "config_update.pb"))
        cmd.append("--type")
        cmd.append("common.ConfigUpdate")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "config_update.json"))
        subprocess.run(cmd, check=True, env=env)

        str = 'echo \'{{"payload":{{"header":{{"channel_header":{{"channel_id":"\'{}\'", "type":2}}}},"data":{{"config_update":\'$(cat {})\'}}}}}}\' | jq . > {}'.format(
            channel_name,
            os.path.join(config_folder_path, "config_update.json"),
            os.path.join(config_folder_path, "config_update_in_envelope.json"),
        )
        subprocess.run(
            [str],
            shell=True,
            check=True,
        )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "config_update_in_envelope.json"))
        cmd.append("--type")
        cmd.append("common.Envelope")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, f"config_update_in_envelope.pb"))
        subprocess.run(cmd, check=True, env=env)

        old_orgs = copy.deepcopy(
            new_network_config["blockchain_peer_config"]["organizations"][
                :new_org_start_index
            ]
        )

        org_index = 0

        for org in old_orgs:
            if org_index == len(old_orgs) - 1:
                break
            sign_configtx(
                network_config=new_network_config,
                fabric_cfg_folder=fabric_cfg_folder,
                nodeIp=nodeIp,
                crypto_config_folder=crypto_config_folder,
                file_path=os.path.join(
                    config_folder_path, f"config_update_in_envelope.pb"
                ),
                org_index=org_index,
            )

            org_index+=1

        submit_update(
            network_config=new_network_config,
            fabric_cfg_folder=fabric_cfg_folder,
            nodeIp=nodeIp,
            crypto_config_folder=crypto_config_folder,
            file_path=os.path.join(config_folder_path, f"config_update_in_envelope.pb"),
            org_index=org_index,
        )

        org_index = new_org_start_index

        fetch_block(
            network_config=new_network_config,
            fabric_cfg_folder=fabric_cfg_folder,
            nodeIp=nodeIp,
            crypto_config_folder=crypto_config_folder,
            block_num=0,
            output_folder=config_folder_path,
            output_file_name=f"{network_name}-appchannel.block",
        )

        for org in new_orgs:
            for peer_index in range(0, org["number_peer"]):

                multiple_retry.multiple_retry(
                    func=join_channel,
                    kwargs={
                        "network_config": new_network_config,
                        "fabric_cfg_folder": fabric_cfg_folder,
                        "nodeIp": nodeIp,
                        "crypto_config_folder": crypto_config_folder,
                        "org_index": org_index,
                        "peer_index": peer_index,
                        "block_path": f"{config_folder_path}/{network_name}-appchannel.block",
                    },
                    num_retry=5,
                )
            org_index += 1

        org_index = new_org_start_index

        for org in new_orgs:
            update_ancher_peer(
                network_config=new_network_config,
                fabric_cfg_folder=fabric_cfg_folder,
                nodeIp=nodeIp,
                crypto_config_folder=crypto_config_folder,
                configtxgen_folder=block_folder,
                org_index=org_index,
                peer_index=0,
            )

            org_index += 1

    except Exception as e:
        print(e)
        raise OperationError(f"Fail to add new organizations")

def remove_organizations(
    new_network_config,
    remove_org_start_index,
    fabric_cfg_folder,
    nodeIp,
    crypto_config_folder,
    configtxgen_folder,
    block_folder,
):
    try:
        network_name = new_network_config["name"]
        channel_name = f"{network_name}-appchannel"

        new_orgs = copy.deepcopy(
            new_network_config["blockchain_peer_config"]["organizations"][
                remove_org_start_index:
            ]
        )

        config_folder_path = os.path.join(
            block_folder, f"remove_org_from{remove_org_start_index}"
        )

        config_pb_file_name = "config_block.pb"
        config_js_file_name = "config_block.json"

        os.makedirs(config_folder_path, exist_ok=True)

        env = dict(
            **os.environ,
        )

        fetch_block(
            network_config=new_network_config,
            fabric_cfg_folder=fabric_cfg_folder,
            nodeIp=nodeIp,
            crypto_config_folder=crypto_config_folder,
            block_num="config",
            output_folder=config_folder_path,
            output_file_name=config_pb_file_name,
        )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_decode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, config_pb_file_name))
        cmd.append("--type")
        cmd.append("common.Block")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, config_js_file_name))
        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                "jq .data.data[0].payload.data.config {} >'{}'".format(
                    os.path.join(config_folder_path, config_js_file_name),
                    os.path.join(config_folder_path, "config.json"),
                )
            ],
            shell=True,
            check=True,
        )

        shutil.copyfile(
            os.path.join(config_folder_path, "config.json"),
            os.path.join(config_folder_path, "temp_config.json"),
        )

        env = dict(
            **os.environ,
            FABRIC_CFG_PATH=f"{configtxgen_folder}",
        )

        for org in new_orgs:

            str = 'jq \'del(.channel_group.groups.Application.groups.{})\' {} > {}'.format(
                f"{org['name'].capitalize()}MSP",
                os.path.join(config_folder_path, "temp_config.json"),
                os.path.join(config_folder_path, "modified_config.json"),
            )

            subprocess.run(
                [str],
                shell=True,
                check=True,
            )

            shutil.copyfile(
                os.path.join(config_folder_path, "modified_config.json"),
                os.path.join(config_folder_path, "temp_config.json"),
            )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "config.json"))
        cmd.append("--type")
        cmd.append("common.Config")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "config.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "modified_config.json"))
        cmd.append("--type")
        cmd.append("common.Config")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "modified_config.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("compute_update")
        cmd.append("--channel_id")
        cmd.append(channel_name)
        cmd.append("--original")
        cmd.append(os.path.join(config_folder_path, "config.pb"))
        cmd.append("--updated")
        cmd.append(os.path.join(config_folder_path, "modified_config.pb"))
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "config_update.pb"))
        subprocess.run(cmd, check=True, env=env)

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_decode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "config_update.pb"))
        cmd.append("--type")
        cmd.append("common.ConfigUpdate")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, "config_update.json"))
        subprocess.run(cmd, check=True, env=env)

        str = 'echo \'{{"payload":{{"header":{{"channel_header":{{"channel_id":"\'{}\'", "type":2}}}},"data":{{"config_update":\'$(cat {})\'}}}}}}\' | jq . > {}'.format(
            channel_name,
            os.path.join(config_folder_path, "config_update.json"),
            os.path.join(config_folder_path, "config_update_in_envelope.json"),
        )
        subprocess.run(
            [str],
            shell=True,
            check=True,
        )

        cmd = []

        cmd.append("configtxlator")
        cmd.append("proto_encode")
        cmd.append("--input")
        cmd.append(os.path.join(config_folder_path, "config_update_in_envelope.json"))
        cmd.append("--type")
        cmd.append("common.Envelope")
        cmd.append("--output")
        cmd.append(os.path.join(config_folder_path, f"config_update_in_envelope.pb"))
        subprocess.run(cmd, check=True, env=env)

        old_orgs = copy.deepcopy(
            new_network_config["blockchain_peer_config"]["organizations"]
        )

        org_index = 0

        for org in old_orgs:
            sign_configtx(
                network_config=new_network_config,
                fabric_cfg_folder=fabric_cfg_folder,
                nodeIp=nodeIp,
                crypto_config_folder=crypto_config_folder,
                file_path=os.path.join(
                    config_folder_path, f"config_update_in_envelope.pb"
                ),
                org_index=org_index,
            )

            org_index+=1
            if org_index == len(old_orgs) - 1:
                break

        submit_update(
            network_config=new_network_config,
            fabric_cfg_folder=fabric_cfg_folder,
            nodeIp=nodeIp,
            crypto_config_folder=crypto_config_folder,
            file_path=os.path.join(config_folder_path, f"config_update_in_envelope.pb"),
            org_index=org_index,
        )

    except Exception as e:
        print(e)
        raise OperationError(f"Fail to remove organizations")
