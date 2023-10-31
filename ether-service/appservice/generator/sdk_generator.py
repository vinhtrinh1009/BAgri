import os
import pathlib
import yaml

from jinja2 import Environment, FileSystemLoader

from constants.config import *
from includes import utils


def gen_code(data_rendering, dir):
    file_loader = FileSystemLoader(os.path.join(base_dir, 'templates/'))
    dapp_name = data_rendering['basic_info']['dapp_name']
    env = Environment(loader=file_loader, autoescape=True)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    
    py_handler = os.path.join(base_dir, f'{dir}/py_handler.py')
    py_handler_template = env.get_template('python_sdk.jinja2')
    utils.gen_file(data=data_rendering, dst=py_handler, template=py_handler_template)

