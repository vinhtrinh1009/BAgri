import os
import time
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader
from fabric_service.const import BASE_DIR
from fabric_service.exceptions import OperationError, ChainCodeOperationError
import subprocess

PRE_ERROR = 0
GENFILE_ERROR = 1
VENDOR_ERROR = 2
PACKAGE_ERROR = 3
INSTALL_ERROR = 4
DEPLOY_CHAINCODE = 5
APPROVE_ERROR = 6
COMMIT_ERROR = 7
INVOKE_ERROR = 8

MAX_DELAY_TIME = 300

def multiple_retry(func, kwargs, num_retry=2, delay=5):
    error = None
    result = None
    for i in range(num_retry):
        try:
            result = func(**kwargs)
        except Exception as e:
            error = e
            if i != num_retry:
                sleep_time = min(delay*(i+1)*2, MAX_DELAY_TIME)
                time.sleep(sleep_time)
        else:
            return result
    if error:
        raise error
    else:
        raise BaseException()

def gen_file(data, dst, template, **kwargs):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    file = open(dst, "w")
    output = template.render(data=data, **kwargs)
    file.write(output)
    file.close()

def get_fabric_cfg_folder_path():
    return os.path.join("/fabric-samples","config")

def get_network_folder_path(username, network_id):
    return os.path.join(
        BASE_DIR,
        "projects",
        username,
        network_id,
    )

def calPeerNodePort(org_index, peer_index):
    return 30000 + (org_index + 1)*100 + (peer_index + 1)

def calPeerCaNodePort(org_index):
    return 30000 + (org_index + 1)*100

def calOrdererNodePort():
    return 30000 + 7

def calOrdererCaNodePort():
    return 30000 + 4

def calExplorerPort():
    return 30000 + 8

def go_mod_vendor(dest_folder):
    try:

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

def packageChaincode( 
    package_folder, temp_folder, network_config, org_index, peer_index, nodeIp, crypto_config_path, fabric_cfg_folder, token_name, token_version
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_path,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_path,
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
            CORE_PEER_ADDRESS=f"{nodeIp}:{calPeerNodePort(org_index, peer_index)}",
        )

        cmd = [
            "peer", "lifecycle", "chaincode", "package", 
            f"{package_folder}",
            "--path", f"{temp_folder}", "--lang", "golang", 
            "--label", f"{token_name}_{token_version}"
        ]

        subprocess.run(cmd, check=True, env=env)

    except Exception as e:
        print(e)
        raise OperationError(f"Fail to package Chaincode")

def installChaincode(network_config, org_index, peer_index, nodeIp, crypto_config_path, fabric_cfg_folder, package_path):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        print(org_index, org_name)
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_path,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_path,
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
            CORE_PEER_ADDRESS=f"{nodeIp}:{calPeerNodePort(org_index, peer_index)}",
        )

        cmd = [
            "peer", "lifecycle", "chaincode", "install",
            package_path
        ]
        subprocess.run(cmd, check=True, env=env)

    except Exception as e:
        print(e)
        raise OperationError(f"Fail to install Chaincode for peer")

def queryInstalled(network_config, org_index, peer_index, nodeIp, crypto_config_path, fabric_cfg_folder, token_name, token_version):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        print(org_index, org_name)
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_path,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_path,
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
            CORE_PEER_ADDRESS=f"{nodeIp}:{calPeerNodePort(org_index, peer_index)}",
        )

        cmd = [
            "peer", "lifecycle", "chaincode", "queryinstalled",
        ]
        result = subprocess.run(
            cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).stdout.decode("utf-8")
        print(result)
        start = result.find(
            f"{token_name}_{token_version}:"
        )
        end = result.find(
            f", Label: {token_name}"
        )

        if start < 0 or end < 0:
            raise OperationError(
                f"Fail to querry chaincode for peer {peer_index} of Organization of index {org_index}"
            )
        print(result[start:end])
        return result[start:end]

    except Exception as e:
        print(e)
        raise OperationError(f"Fail to get package ID")

def approveChaincode(network_config, org_index, peer_index, nodeIp, crypto_config_path, fabric_cfg_folder, token_name, token_version, package_id):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        print(org_index, org_name)
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_path,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_path,
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
            CORE_PEER_ADDRESS=f"{nodeIp}:{calPeerNodePort(org_index, peer_index)}",
        )

        cmd = [
            "peer", "lifecycle", "chaincode", "approveformyorg", 
            "-o", orderer_url, "--ordererTLSHostnameOverride",
            f"orderer.{network_name}.com", "--tls", "--cafile",
            orderer_ca, "--channelID", channel_name, "--name",
            token_name, "--version", str(token_version), "--sequence",
            str(token_version), "--package-id", package_id, "--init-required"
        ]
        subprocess.run(cmd, env=env, check=True)

    except Exception as e:
        print(e)
        raise OperationError(f"Fail to approve for organization of index {org_index}")

def commitChaincode(network_config, nodeIp, crypto_config_path, fabric_cfg_folder, token_name, token_version):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][0]["name"]
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_path,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_path,
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
            CORE_PEER_ADDRESS=f"{nodeIp}:{calPeerNodePort(0, 0)}",
        )

        cmd = [
            "peer", "lifecycle", "chaincode", "commit",
            "-o", orderer_url, "--ordererTLSHostnameOverride",
            f"orderer.{network_name}.com", "--tls", "--cafile",
            orderer_ca, "--channelID", channel_name, "--name",
            token_name, "--version", str(token_version), "--sequence",
            str(token_version)
        ]

        org_index = 0

        for org in network_config["blockchain_peer_config"]["organizations"]:
            cmd.append("--peerAddresses")
            cmd.append(f"{nodeIp}:{calPeerNodePort(org_index, 0)}")

            org_crypto_config_folder = os.path.join(
                crypto_config_path,
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
        cmd.append("--init-required")

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to Commit Chaincode Definition")

def invokeChaincode(network_config, nodeIp, crypto_config_path, fabric_cfg_folder, token_name, token_version):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][0]["name"]
        channel_name = f"{network_name}-appchannel"

        orderer_url = f"{nodeIp}:{calOrdererNodePort()}"

        orderer_ca = os.path.join(
            crypto_config_path,
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
            "msp",
            "tlscacerts",
            f"tlsca.{network_name}.com-cert.pem",
        )

        org_crypto_config_folder = os.path.join(
            crypto_config_path,
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
            CORE_PEER_ADDRESS=f"{nodeIp}:{calPeerNodePort(0, 0)}",
        )

        cmd = [
            "peer", "chaincode", "invoke",
            "-o", orderer_url, "--ordererTLSHostnameOverride",
            f"orderer.{network_name}.com", "--tls", "--cafile",
            orderer_ca, "-C", channel_name, "-n",
            token_name,
        ]

        org_index = 0

        for org in network_config["blockchain_peer_config"]["organizations"]:
            cmd.append("--peerAddresses")
            cmd.append(f"{nodeIp}:{calPeerNodePort(org_index, 0)}")

            org_crypto_config_folder = os.path.join(
                crypto_config_path,
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
        cmd.append("--isInit")
        cmd.append("-c")
        cmd.append('{"function":"Init","Args":[]}')

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(f"Fail to invoke Chaincode")


async def generate_chaincode_file(chaincode_config, 
                        network_config, 
                        chaincode_folder, 
                        user_info, 
                        kube_config_path, chaincode_version, nodeIp):
    # username = user_info['username']
    print(BASE_DIR)
    file_loader = FileSystemLoader(BASE_DIR +'/templates')
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    env.globals["calPeerNodePort"] = calPeerNodePort
    env.globals["calPeerCaNodePort"] = calPeerCaNodePort
    env.globals["calOrdererNodePort"] = calOrdererNodePort
    env.globals["calOrdererCaNodePort"] = calOrdererCaNodePort

    network_folder = get_network_folder_path(user_info['username'], network_config['network_id'])
    crypto_config_folder = f"{network_folder}/crypto-config"

    cfg_folder = get_fabric_cfg_folder_path()

    chaincode_path = chaincode_folder + f"/chaincode/token.go"
    chaincode_template = env.get_template("erc20_template.jinja2")
    gen_file(
        data={
            "name": chaincode_config['token_name'],
            "initialSupply": chaincode_config['initial_supply'],
            "symbol": chaincode_config['token_symbol'],
            "decimal": chaincode_config['decimal']
        },
        dst=chaincode_path,
        template=chaincode_template,
    )
    erc20_folder = BASE_DIR+f"/erc20"
    shutil.copytree(erc20_folder, os.path.dirname(chaincode_path), dirs_exist_ok=True)

    script_utils = chaincode_folder + f"/scripts/script_utils.sh"
    script_utils_template = env.get_template("script_utils_template.jinja2")
    gen_file(
        data={}, dst=script_utils, template=script_utils_template
    )

    deploy_chaincode = chaincode_folder + f"/scripts/deploy_chaincode.sh"
    deploy_chaincode_template = env.get_template(
        "deploy_chaincode_template.jinja2"
    )
    temp_folder = BASE_DIR+f"/chaincode/{user_info['username']}/{chaincode_config['token_name']}"
    shutil.copytree(os.path.dirname(chaincode_path), temp_folder)
    # gen_file(
    #     data={
    #         "network_name": network_config["name"],
    #         "orgs": network_config["blockchain_peer_config"]["organizations"],
    #         "token_name": chaincode_config["token_name"],
    #         "temp_folder": temp_folder,
    #         "chaincode_version": chaincode_version,
    #         'nodeIp': nodeIp,
    #         "cfg_folder": cfg_folder,
    #         "network_folder": network_folder
    #     },
    #     dst=deploy_chaincode,
    #     template=deploy_chaincode_template,
    # )
    try: 
        multiple_retry(
            go_mod_vendor,
            kwargs={
                "dest_folder": temp_folder
            }
        )
        package_path=f"{network_folder}/dapps/{chaincode_config['token_name']}/chaincode/${chaincode_config['token_name']}.tar.gz"
        multiple_retry(
            packageChaincode,
            kwargs={
                "package_folder": package_path,
                "temp_folder": temp_folder,
                "network_config": network_config, 
                "org_index": 0, 
                "peer_index": 0, 
                "nodeIp": nodeIp, 
                "crypto_config_path": crypto_config_folder, 
                "fabric_cfg_folder": cfg_folder, 
                "token_name": chaincode_config['token_name'],
                "token_version": chaincode_version
            }
        )
        org_index=0
        
        for org in network_config["blockchain_peer_config"]["organizations"]:
            multiple_retry(
                installChaincode,
                kwargs={
                "network_config": network_config, 
                "org_index": org_index, 
                "peer_index": 0, 
                "nodeIp": nodeIp, 
                "crypto_config_path": crypto_config_folder, 
                "fabric_cfg_folder": cfg_folder, 
                "package_path": package_path
                }
            )
            org_index+=1
        
        org_index = 0
        for org in network_config["blockchain_peer_config"]["organizations"]:
            package_id=multiple_retry(
                    queryInstalled,
                    kwargs={
                    "network_config": network_config, 
                    "org_index": org_index, 
                    "peer_index": 0, 
                    "nodeIp": nodeIp, 
                    "crypto_config_path": crypto_config_folder, 
                    "fabric_cfg_folder": cfg_folder, 
                    "token_name": chaincode_config['token_name'],
                    "token_version": chaincode_version
                    }
                )
            org_index+=1
        
        org_index=0
        for org in network_config["blockchain_peer_config"]["organizations"]:
            multiple_retry(
                approveChaincode,
                kwargs={
                    "network_config": network_config, 
                    "org_index": org_index, 
                    "peer_index": 0, 
                    "nodeIp": nodeIp, 
                    "crypto_config_path": crypto_config_folder,
                    "fabric_cfg_folder": cfg_folder, 
                    "token_name": chaincode_config['token_name'], 
                    "token_version": chaincode_version, 
                    "package_id": package_id,
                },
                num_retry=5
            )
            org_index+=1
        
        multiple_retry(
            commitChaincode,
            kwargs={
                "network_config": network_config, 
                "nodeIp": nodeIp, 
                "crypto_config_path": crypto_config_folder, 
                "fabric_cfg_folder": cfg_folder, 
                "token_name": chaincode_config['token_name'], 
                "token_version": chaincode_version
            },
            num_retry=5
        )

        multiple_retry(
            invokeChaincode,
            kwargs={
                "network_config": network_config, 
                "nodeIp": nodeIp, 
                "crypto_config_path": crypto_config_folder, 
                "fabric_cfg_folder": cfg_folder, 
                "token_name": chaincode_config['token_name'], 
                "token_version": chaincode_version
            },
            num_retry=5
        )
    except OperationError as e:
        return False

    # process = subprocess.run(f"bash {deploy_chaincode}", shell=True)
    # if process.returncode != 0:
    #     return False
    shutil.rmtree(temp_folder, ignore_errors=True)
    return True
