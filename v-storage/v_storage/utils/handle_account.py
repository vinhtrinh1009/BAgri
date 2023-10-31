import requests
import json
from settings import config

BASE_ACCOUNT_URL = config['account_service']['host']
BASE_CORE_SERVICE_URL = config['core_service']['host']

def get_token():
    url = f"{BASE_ACCOUNT_URL}/login"
    payload = json.dumps({
        "username": config['account_service']['username'],
        "password": config['account_service']['password']
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.content.decode("utf8"))

def get_info_by_sdk_key(token, sdk_key):
    url = f"{BASE_CORE_SERVICE_URL}/sdks/{sdk_key}"
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.content.decode("utf8"))