import requests
import json
from settings import config as cfg
from exceptions import AccountServiceRequestError

BASE_ACCOUNT_URL = cfg['account_service']['host']

def get_token():
    url = f"{BASE_ACCOUNT_URL}/login"
    payload = json.dumps({
        "username": cfg['account_service']['username'],
        "password": cfg['account_service']['password']
    })
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.content.decode("utf8"))["data"]["token"]
    except Exception as e:
        raise AccountServiceRequestError("Error while login")
