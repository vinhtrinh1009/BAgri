import os
import time
import yaml
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from fabric_service.const import BASE_DIR

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

async def generate_sdk(token_name, user_info, network_id, network_config):
    network_folder = get_network_folder_path(user_info['username'], network_id)
    network_name = network_config["name"]
    org_name = network_config["blockchain_peer_config"]["organizations"][0]["name"]
    owner_cert_path = os.path.join(
        network_folder,
        "crypto-config",
        "peerOrganizations",
        f"{org_name}.{network_name}.com",
        "users",
        f"Admin@{org_name}.{network_name}.com",
        "msp",
        "signcerts",
        f"Admin@{org_name}.{network_name}.com-cert.pem",
    )
    owner_cert=""
    with open(owner_cert_path, "r") as owner_cert_file:
        for readline in owner_cert_file:
            # if readline.strip() == "-----BEGIN CERTIFICATE-----" or readline.strip()=="-----END CERTIFICATE-----":
            #     continue
            owner_cert+=readline
    owner_cert = repr(owner_cert)
    owner_privkey_path = os.path.join(
        network_folder,
        "crypto-config",
        "peerOrganizations",
        f"{org_name}.{network_name}.com",
        "users",
        f"Admin@{org_name}.{network_name}.com",
        "msp",
        "keystore",
        "priv_sk",
    )
    owner_privkey=""
    with open(owner_privkey_path, "r") as owner_privkey_file:
        newline_break=""
        for readline in owner_privkey_file:
            # if readline.strip() == "-----BEGIN PRIVATE KEY-----"  or readline.strip()=="-----END PRIVATE KEY-----":
            #     continue
            owner_privkey+=readline
    owner_privkey = repr(owner_privkey)
    file_loader = FileSystemLoader(BASE_DIR +'/templates')
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    output_dir = os.path.join(BASE_DIR, "data", user_info['username'], network_id, token_name, "sdk")
    shutil.rmtree(output_dir, ignore_errors=True)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    registerUser_template = env.get_template("sdk/cli/registerUser.jinja2")
    gen_file(data={}, dst=os.path.join(output_dir, "cli/registerUser.js"), template=registerUser_template)
    enrollOwner_template = env.get_template("sdk/cli/enrollOwner.jinja2")
    gen_file(
        data={
            "org": org_name
        }, 
        dst=os.path.join(output_dir, "cli/enrollOwner.js"), 
        template=enrollOwner_template
    )
    enrollAdmin_template = env.get_template("sdk/cli/enrollAdmin.jinja2")
    gen_file(
        data={},
        dst=os.path.join(output_dir, "cli/enrollAdmin.js"),
        template=enrollAdmin_template
    )
    example_template = env.get_template("sdk/cli/example.jinja2")
    gen_file(
        data={
            'org': org_name
        }, 
        dst = os.path.join(output_dir, "cli/example.js"), 
        template=example_template
    )
    config_template = env.get_template("sdk/config.jinja2")
    gen_file(
        data={
            'owner_cert': owner_cert,
            'owner_privkey': owner_privkey
        },
        dst=os.path.join(output_dir, "config.js"),
        template=config_template
    )
    network_template = env.get_template("sdk/fabric/network.jinja2")
    gen_file(
        data={
            'network_name': network_name,
            'token_name': token_name,
            'org': org_name,
        },
        dst=os.path.join(output_dir, "fabric/network.js"),
        template=network_template
    )
    package_template = env.get_template("sdk/package.jinja2")
    gen_file(
        data={
            'token_name': token_name
        },
        dst=os.path.join(output_dir, "package.json"),
        template=package_template
    )
    connection_files_path = os.path.join(network_folder, "connection-files/ccp.json")
    ccp_dest_path = os.path.join(output_dir, "connection-files")
    Path(ccp_dest_path).mkdir(parents=True, exist_ok=True)
    shutil.copy(connection_files_path, ccp_dest_path)
    return output_dir





    