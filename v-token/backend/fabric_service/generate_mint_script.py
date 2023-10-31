import os
import time
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader
from fabric_service.const import BASE_DIR
import subprocess

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

async def generate_mint_file(chaincode_config, 
                        network_config, 
                        user_info, nodeIp, quantity, minter_org, minter_username):
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
    cfg_folder = get_fabric_cfg_folder_path()

    invoke_chaincode_mint_template = env.get_template(
        "invoke_chaincode_mint.jinja2"
    )
    invoke_chaincode_mint = BASE_DIR+f"/chaincode/{user_info['username']}/{chaincode_config}/scripts/invoke_chaincode_mint.sh"
    if os.path.exists(invoke_chaincode_mint):
            os.remove(invoke_chaincode_mint)
    gen_file(
        data={
            "network_name": network_config["name"],
            "orgs": network_config["blockchain_peer_config"]["organizations"],
            "token_name": chaincode_config,
            "temp_folder": invoke_chaincode_mint,
            'nodeIp': nodeIp,
            "cfg_folder": cfg_folder,
            "network_folder": network_folder,
            "quantity": quantity,
            "minter_org": minter_org,
            "minter_username": minter_username
        },
        dst=invoke_chaincode_mint,
        template=invoke_chaincode_mint_template,
    )

    # os.system(
    #     f"kubectl --kubeconfig {kube_config_path} exec -i fabric-tools -- /bin/bash /fabric/dapps/{chaincode_config['token_name']}/scripts/deploy_chaincode.sh"
    # )

    process = subprocess.run(f"bash {invoke_chaincode_mint}", shell=True)
    if process.returncode != 0:
        return False
    
    return True