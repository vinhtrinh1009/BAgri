import os
import asyncio
import random
import string
import hashlib
from jinja2 import Environment, FileSystemLoader
from fabric_service.const import BASE_DIR
import subprocess
from django.conf import settings
from web3 import Web3
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware
import json

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

def get_random_int():
    # letters = string.ascii_lowercase
    # result_str = ''.join(random.choice(letters) for i in range(20))
    result_int = random.randint(0, 10000000)
    return result_int

async def generate_burn_file(chaincode_config, 
                        network_config, 
                        user_info, nodeIp, quantity, token_address, to_address):
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

    # invoke_chaincode_mint = chaincode_folder + f"/scripts/invoke_chaincode_mint.sh"
    invoke_chaincode_burn_template = env.get_template(
        "invoke_chaincode_burn.jinja2"
    )
    invoke_chaincode_burn = BASE_DIR+f"/chaincode/{user_info['username']}/{chaincode_config}/scripts/invoke_chaincode_mint.sh"
    if os.path.exists(invoke_chaincode_burn):
            os.remove(invoke_chaincode_burn)
    gen_file(
        data={
            "network_name": network_config["name"],
            "orgs": network_config["blockchain_peer_config"]["organizations"],
            "token_name": chaincode_config,
            "temp_folder": invoke_chaincode_burn,
            'nodeIp': nodeIp,
            "cfg_folder": cfg_folder,
            "network_folder": network_folder,
            "quantity": quantity
        },
        dst=invoke_chaincode_burn,
        template=invoke_chaincode_burn_template,
    )

    process = subprocess.run(f"bash {invoke_chaincode_burn}", shell=True)
    if process.returncode != 0:
        return False
    
    
    web3ConnectRinkeby({'toTokenAddress': token_address, 'amount': quantity, 'to': to_address})

    
    return True

def web3ConnectRinkeby(args):
    rinkeby_bridge_address = settings.RINKEBY_BRIDGE_CONTRACT_ADDRESS_V2
    rinkeby_web3 = Web3(Web3.HTTPProvider(settings.INFURA_RINKEBY_HTTP_URL))
    abi = None
    with open(settings.RINKEBY_BRIDGE_CONTRACT_ABI_FILEPATH_V2) as f:
        abi = json.loads(f.read())
    rinkeby_bridge_contract = rinkeby_web3.eth.contract(address=rinkeby_bridge_address, abi=abi)
    rand = get_random_int()
    nonce = rand
    token_address = args['toTokenAddress']
    func = rinkeby_bridge_contract.functions.mint(token_address, args['to'], args['amount'], nonce)
    try:
        tx = func.buildTransaction({
            # 'gas': 70000,
            # 'gasPrice': self.rinkeby_web3.eth.gas_price,
            'from': settings.RINKEBY_BRIDGE_ADMIN_ADDRESS,
            'nonce': rinkeby_web3.eth.getTransactionCount(settings.RINKEBY_BRIDGE_ADMIN_ADDRESS)
        })
    except ContractLogicError as e:
        print(e)
        return

    # sign transaction
    private_key = rinkeby_web3.toHex(hexstr=settings.ETHEREUM_PRIVATE_KEY)
    signed_tx = rinkeby_web3.eth.account.sign_transaction(tx, private_key=private_key)

    # send transaction
    rinkeby_web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Send mint transaction for {args['to']} with amount {args['amount']}")