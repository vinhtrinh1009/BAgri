from collections import namedtuple
import os
import subprocess
import requests
import json

from settings import config as cfg
from exceptions import GitlabServiceRequestError


def get_groups(group_name, parent_group_id):
    try:
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
    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to get group {group_name}")


def create_group(name, parent_id):
    try:
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
    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to create group {name}")


def create_project(name, namespace_id):
    try:
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
    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to create group {name}")


def create_variable(name, value, group_id, type_env="file"):
    try:
        url = (
            "https://gitlab.com/api/v4/groups/"
            + str(group_id)
            + "/variables?private_token="
            + cfg["gitlab"]["private_token"]
        )
        data = {"key": name, "value": value, "variable_type": type_env}
        response = requests.post(url, data=data)
    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to create variable {name}")


def push(file_path, project_path, commit_message, private_token):
    try:
        subprocess.run(
            [
                'cd {} && git init && git add . && git commit -m "{}" && git remote add origin {} && git push origin master'.format(
                    file_path,
                    commit_message,
                    f"https://oauth2:{private_token}@gitlab.com/{project_path}.git",
                )
            ],
            shell=True,
            check=True,
        )
    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to push {file_path}")

def pull(file_path, project_path, private_token):
    try:
        subprocess.run(
            [
                'cd {} && git init && git remote add origin {} && git pull origin master'.format(
                    file_path,
                    f"https://oauth2:{private_token}@gitlab.com/{project_path}.git",
                )
            ],
            shell=True,
            check=True,
        )
    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to pull to {file_path}")


def push_without_create(file_path, commit_message):
    try:
        subprocess.run(
            [
                'cd {} && git add . && git commit -m "{}" && git push origin master'.format(
                    file_path,
                    commit_message,
                )
            ],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to push {file_path}")


def delete_group(namespace_id):
    try:
        url = (
            "https://gitlab.com/api/v4/groups/"
            + str(namespace_id)
            + "?private_token="
            + cfg["gitlab"]["private_token"]
        )
        response = requests.delete(url)
        return response.content.decode("utf8")
    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to delete group {str(namespace_id)}")

def search_project(project_name, group_id):
    try:
        url = (
            "https://gitlab.com/api/v4/groups/"
            + str(group_id)
            + "/search?private_token="
            + cfg["gitlab"]["private_token"]
            + "&scope=projects&search="
            + project_name
        )
        response = requests.get(url)
        groups = json.loads(response.content.decode("utf-8"))
        return groups
    except Exception as e:
        raise GitlabServiceRequestError(f"Fail to search project {project_name}")


def gen_deploy_token(group_id):
    try:
        url = (
            "https://gitlab.com/api/v4/groups/"
            + str(group_id)
            + "/deploy_tokens?private_token="
            + cfg["gitlab"]["private_token"]
        )
        token_info = {
            "name": "My deploy token",
            "scopes": ["read_repository", "read_registry"],
        }
        response = requests.post(url, json=token_info)
        newtoken = json.loads(response.content.decode("utf-8"))
        return newtoken
    except Exception as e:
        raise GitlabServiceRequestError(
            f"Fail to gen deploy token in project {group_id}"
        )


def get_piplines(project_id):
    try:
        url = (
            "https://gitlab.com/api/v4/projects/"
            + str(project_id)
            + "/pipelines?private_token="
            + cfg["gitlab"]["private_token"]
        )
        response = requests.get(url)
        piplines = json.loads(response.content.decode("utf-8"))
        return piplines
    except Exception as e:
        raise GitlabServiceRequestError(
            f"Fail to get pipline status in project {project_id}"
        )
