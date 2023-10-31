import pathlib
import yaml
import os

DRIVER_DIR = pathlib.Path(__file__).parent.parent
project_path = DRIVER_DIR / 'projects'

config_file = os.environ.get("CONFIG_FILE", "develop.yaml")
config_path = DRIVER_DIR / 'config' / config_file


def get_config(path):
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


config = get_config(config_path)
