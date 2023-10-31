from logging import Logger
import subprocess
from config.logging_config import get_logger
from exceptions import (
    GitlabError,
)

_LOGGER = get_logger(__name__)
def push_without_create(file_path, commit_message):
    try:
        cmd = []

        cmd.append("cd")

        cmd.append(file_path)

        cmd.append(f"&& git add . && git commit -m '{commit_message}' && git push")

        result = subprocess.run(cmd, check=True)

    except Exception as e:
        raise GitlabError(f"Fail to push {file_path}")

def push(file_path, project_path, commit_message, private_token):
    try:
        cmd = []
        cmd.append("cd")
        cmd.append(file_path)
        cmd.append('&&')
        cmd.append('git init && git add . ')
        cmd.append('&&')
        cmd.append(f"git commit -m '{commit_message}'")
        cmd.append('&&')
        cmd.append(f"git remote add origin https://oauth2:{private_token}@gitlab.com/{project_path}.git && git push --set-upstream origin master")
        result = subprocess.run(cmd, check=True)
    except Exception as e:
        raise GitlabError(f"Fail to push {file_path}")   