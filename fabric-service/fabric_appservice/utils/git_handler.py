import os
import requests
import json

from settings import config as cfg


def get_groups(group_name, parent_group_id):
    url = (
        "https://gitlab.com/api/v4/groups/"
        + str(parent_group_id)
        + "/subgroups?private_token="
        + cfg["gitlab"]["private_token"]
        + "&search="
        + group_name
    )
    response = requests.get(url)
    groups = json.loads(response.content.decode("utf-8"))
    return groups


def create_group(name, parent_id):
    url = (
        "https://gitlab.com/api/v4/groups?private_token="
        + cfg["gitlab"]["private_token"]
        + "&path="
        + name
        + "&name="
        + name
        + "&parent_id="
        + str(parent_id)
    )
    response = requests.post(url)
    content = json.loads(response.content.decode("utf8"))
    group_id = content["id"]
    return group_id


def create_project(name, namespace_id):
    url = (
        "https://gitlab.com/api/v4/projects?path="
        + name
        + "&private_token="
        + cfg["gitlab"]["private_token"]
        + "&namespace_id="
        + str(namespace_id)
    )
    response = requests.post(url)
    content = response.content.decode("utf8")
    content_dict = json.loads(content)
    return content_dict


def create_variable(name, value, group_id, type_env="file"):
    url = (
        "https://gitlab.com/api/v4/groups/"
        + str(group_id)
        + "/variables?private_token="
        + cfg["gitlab"]["private_token"]
    )
    data = {"key": name, "value": value, "variable_type": type_env}
    response = requests.post(url, data=data)


def git_push_without_create(rest_api_path, processor_path):
    cmd = (
        "cd "
        + rest_api_path
        + " && git add . && git commit -m 'delete app' && git push"
    )
    os.system(cmd)
    cmd = (
        "cd "
        + processor_path
        + " && git add . && git commit -m 'deleteapp' && git push"
    )
    os.system(cmd)


def delete_group(namespace_id):
    url = (
        "https://gitlab.com/api/v4/groups/"
        + str(namespace_id)
        + "?private_token="
        + cfg["gitlab"]["private_token"]
    )
    response = requests.delete(url)
    return response.content.decode("utf8")


def git_clone_project(name, deploy_token, project_url):
    cmd = (
        "git clone https://"
        + name
        + ":"
        + deploy_token
        + "@gitlab.com/"
        + project_url
        + ".git"
    )
    os.system(cmd)
