import requests
import json
import os
from settings import config
from exceptions import StorageServiceRequestError

BASE_STORAGE_URL = config['v_storage']['host']

def get_user_folder(token):
    url = f"{BASE_STORAGE_URL}/folders"
    headers = {
        'Authorization': 'Bearer ' + token
    }
    try:
        response = requests.request(
            method = "GET",
            url = url,
            headers = headers
        )
        return json.loads(response.content.decode("utf8"))["data"]["user_folder"]
    except Exception:
        raise StorageServiceRequestError("Error while get folder")

def get_folder(token, folder_id):
    url = f"{BASE_STORAGE_URL}/folders/{folder_id}"

    headers = {
        'Authorization': 'Bearer ' + token
    }

    try:
        response = requests.request(
            method = "GET",
            url = url,
            headers = headers
        )
        return json.loads(response.content.decode("utf8"))["data"]["folder"]
    except Exception:
        raise StorageServiceRequestError("Error while get folder")

def create_folder(token, payload):
    url = f"{BASE_STORAGE_URL}/folders"
    body = json.dumps({
        "name": payload["name"],
        "parent_id": payload["parent_id"],
        "shared": payload["shared"]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ token
    }
    
    try:
        response = requests.request(
            method = "POST",
            url = url,
            headers = headers,
            data = body
        )
        return json.loads(response.content.decode("utf8"))["data"]["folder"]["folder_id"]
    except Exception:
        raise StorageServiceRequestError("Error while create folder")

def upload_folder(token, parent_id, shared, folder_path):
    url = f"{BASE_STORAGE_URL}/folders/{parent_id}/upload"
    folder_name = folder_path.split('/')[-1]
    os.chdir(folder_path)
    list_files = []

    for (root, dirs, files) in os.walk(folder_path, topdown=True):
        for file in files:
            if not os.path.isdir(f"{root}/{file}"):
                list_files.append({
                    "name": f"{folder_name}{root.replace(folder_path, '')}/{file}",
                    "path": f"{root}/{file}"
                })

    files = {}
    for i in range(len(list_files)):
        files[f"upload_folder[{i}]"] = (list_files[i]["name"], open(list_files[i]["path"], 'rb'))

    data = {"shared": shared}
    
    headers = {'Authorization': 'Bearer ' + token}
    
    try:
        response = requests.request(
            method = "POST",
            url = url,
            headers = headers,
            files = files,
            data = data
        )

        return json.loads(response.content.decode("utf8"))
    except Exception:
        raise StorageServiceRequestError("Error while upload folder")

def delete_folder(token, folder_id):
    url = f"{BASE_STORAGE_URL}/folders/{folder_id}/delete"

    headers = {
        'Authorization': 'Bearer ' + token
    }

    try:
        response = requests.request(
            method = "DELETE",
            url = url,
            headers = headers
        )
        return json.loads(response.content.decode("utf8")) 
    except Exception:
        raise StorageServiceRequestError("Error while delete folder")
