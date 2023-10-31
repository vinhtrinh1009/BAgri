import os

from jinja2 import Environment, FileSystemLoader

from constants import BASE_DIR
from includes import utils
from settings import config
from config.logging_config import get_logger

_LOGGER = get_logger(__name__)

def gen_code(data, dst_folder):
    # create folder
    processor_folder = os.path.join(
        BASE_DIR, '{0}/{1}/{2}processor/'.format(dst_folder, data['basic_info']['dapp_name'],
                                                 data['basic_info']['dapp_name']),
    )

    if not os.path.exists(processor_folder):
        os.makedirs(processor_folder)

    file_loader = FileSystemLoader(os.path.join(BASE_DIR, 'templates/processor'))

    env = Environment(loader=file_loader, autoescape=True)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    # Generate main file
    main = processor_folder + 'main.py'
    main_template = env.get_template('main_template.jinja2')
    utils.gen_file(data=data, dst=main, template=main_template)

    # Generate handler file
    handler = processor_folder + 'handler.py'
    handler_template = env.get_template('handler_template.jinja2')
    utils.gen_file(data=data, dst=handler, template=handler_template)

    # Generate state file
    state = processor_folder + 'state.py'
    state_template = env.get_template('state_template.jinja2')
    utils.gen_file(data=data, dst=state, template=state_template)

    # Generate payload file
    payload = processor_folder + 'payload.py'
    payload_template = env.get_template('payload_template.jinja2')
    utils.gen_file(data=data, dst=payload, template=payload_template)

    # Generate docker file
    dockerfile = os.path.join(
        BASE_DIR,
        '{0}/{1}/{2}processor/Dockerfile'.format(dst_folder, data['basic_info']['dapp_name'],
                                                 data['basic_info']['dapp_name'])
    )
    
    dockerfile_template = env.get_template('Dockerfile_template.jinja2')
    utils.gen_file(data=data, dst=dockerfile, template=dockerfile_template)

    # Generate yaml file
    processor_yaml = processor_folder + 'processor.yaml'
    processor_yaml_template = env.get_template('proccessoryaml.jinja2')
    utils.gen_file(data=data, dst=processor_yaml, template=processor_yaml_template)

    gitlab_cid = processor_folder + '.gitlab-ci.yml'
    gitlab_cid_template = env.get_template('gitlab_ci_yml.jinja2')
    utils.gen_file(data={'processor_project_name': data['basic_info']['dapp_name'] + "processor",
                         'gitlab_username': config['gitlab_pull_dapp_image']['username'],
                         'gitlab_password': config['gitlab_pull_dapp_image']['password'],
                         'dapp_version': data['basic_info']['dapp_version']},
                   dst=gitlab_cid,
                   template=gitlab_cid_template)
                   
    _LOGGER.debug(f"Generated processor: {processor_folder}")