import requests
import json
from settings import config as cfg

BASE_ACCOUNT_URL = cfg['account_service']['host']

def get_token():
    url = f"{BASE_ACCOUNT_URL}/login"
    payload = json.dumps({
        "username": cfg['account_service']['username'],
        "password": cfg['account_service']['password']
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.content.decode("utf8"))

def get_user_info(token, user_id):
    url = f"{BASE_ACCOUNT_URL}/users/{user_id}"
    headers = {'Authorization': 'Bearer '+ token}
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.content.decode("utf8"))

def update_user_info(token, user_id, **kwargs):
    body = {}
    if "folder_id" in kwargs:
        body["folder_id"] = kwargs["folder_id"]
    url = f"{BASE_ACCOUNT_URL}/users/{user_id}"
    body = json.dumps(body)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ token
    }
    response = requests.request("PUT", url, headers=headers, data=body)
    return json.loads(response.content.decode("utf8"))
