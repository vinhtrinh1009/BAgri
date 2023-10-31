import sys

import asyncio

from settings import config
from config.logging_config import get_logger
# from database import Database

from settings import config
import os
import constants
import subprocess
from operation import k8s_operation, gitlab_operation

# dtb = Database(host=config["database"]["host"],
#                     port=config["database"]["port"],
#                     username=config["database"]["username"],
#                     password=config["database"]["password"],
#                     dbname=config["database"]["db_name"])

# list_dapp = dtb.get_dapps(network_id="61985bf1b451922414fd1270")
# for dapp in list_dapp:
#     print(dapp)

sdk_path = os.path.join(constants.BASE_DIR,'application/usertest/newdapptest110/newdapptest110sdk/')
print(sdk_path)

# commit_message = "create dapp"
# project_path = "test-application/usertest/newdapptest110/newdapptest110sdk"
# gitlab_operation.push(file_path=sdk_path, project_path=project_path,commit_message=commit_message, private_token=config['gitlab']["private_token"])
# test = subprocess.run(["bash", "./sleep.sh"], check=True, stdout=subprocess.PIPE)
# check = test.stdout.decode("utf-8")
# print(check)
list_files = subprocess.run(["cd", sdk_path], stdout=subprocess.DEVNULL)
print(list_files)