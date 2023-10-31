from settings import BASE_DIR, config
import requests
import json
import os

ipfs_url = f'http://{config["ipfs"]["host"]}:{config["ipfs"]["port"]}'
ipfs_daemon_url = config["ipfs_daemon"]["host"]

async def save_file_to_ipfs(file_path, file_name):
    files = [
        ('file', (file_name, open(f'{file_path}', 'rb')))
    ]
    response = requests.request("POST", f"{ipfs_url}/add", files=files)
    res = json.loads(response.text)
    file_cid = res["cid"]["/"]
    return file_cid

async def download_file_from_ipfs(file_cid, save_to_path):
    os.system(f'wget {ipfs_daemon_url}/ipfs/{file_cid} -O {save_to_path}')

async def delete_file_on_ipfs(file_cid):
    res_unpin = requests.request("DELETE", f"{ipfs_url}/pins/{file_cid}")
    res_gc = requests.request("POST", f"{ipfs_url}/ipfs/gc")