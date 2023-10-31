import os

from jinja2 import Environment, FileSystemLoader

from constants import BASE_DIR
from includes import utils
from settings import config
from config.logging_config import get_logger

_LOGGER = get_logger(__name__)

def gen_code(data, dst_folder):
    # create folder
    resource_folder = os.path.join(
        BASE_DIR, '{0}/{1}/'.format(dst_folder, data['resource_info']['resource_name']),
    )
    if not os.path.exists(resource_folder):
        os.makedirs(resource_folder)
    
    file_loader = FileSystemLoader(os.path.join(BASE_DIR, 'templates/resource'))
    env = Environment(loader=file_loader, autoescape=True)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    # gen new node file
    main = resource_folder + 'sawtooth-node.yaml'
    if data['resource_info']['consensus'] == "PBFT" or data['resource_info']['consensus'] == "pbft":         
        main_template = env.get_template('sawtooth-pbft-node.jinja2')
        utils.gen_file(data=data, dst=main, template=main_template)
    else:
        main_template = env.get_template('sawtooth-poet-node.jinja2')
        utils.gen_file(data=data, dst=main, template=main_template)

    
    # main1 = resource_folder + 'dapp-default.yaml'
    # data_dapps = {
    #     "dapps" : data["dapps"],
    #     "username": data["user_info"]["username"],
    #     "host": data["resource_info"]["resource_config"]["host"]
    # }
    # main_template = env.get_template('dapp-default.jinja2')
    # utils.gen_file(data=data_dapps, dst=main1, template=main_template)
    data_makefile = {
        "token" : data["user_info"]["deploy_token"]["token"],
        "username": data["user_info"]["deploy_token"]["username"]
    }
    main2 = resource_folder + "Makefile"
    main_template = env.get_template('Makefile.jinja2')
    utils.gen_file(data=data_makefile, dst=main2, template=main_template)
    
    
    # for dapp in data["dapps"]:
    #     dapp_folder = os.path.join(
    #         BASE_DIR, '{0}/{1}/'.format(resource_folder, dapp["dapp_name"]),
    #     )
    #     if not os.path.exists(dapp_folder):
    #         os.makedirs(dapp_folder)
    #     main1 = dapp_folder + 'dapp-default.yaml'
    #     data_dapp = {
    #         "dapp_name" : dapp["dapp_name"],
    #         "username": data["user_info"]["username"],
    #         "host": data["resource_info"]["resource_config"]["host"]
    #     }
    #     # if data['resource_info']['consensus'] == "PBFT":             
    #     #     main_template = env.get_template('dapp-default-pbft.jinja2')
    #     #     utils.gen_file(data=data_dapp, dst=main1, template=main_template)
    #     # else:
    #     main_template = env.get_template('dapp-default.jinja2')
    #     utils.gen_file(data=data_dapp, dst=main1, template=main_template)
    #     data_makefile = {
    #         "token" : dapp["token"],
    #         "username": dapp["username"]
    #     }
    #     main2 = dapp_folder + "Makefile"
    #     main_template = env.get_template('Makefile.jinja2')
    #     utils.gen_file(data=data_makefile, dst=main2, template=main_template)
