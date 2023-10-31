from celery import Celery
import yaml
import pathlib
import os
from settings import config


# PATH = pathlib.Path(__file__).parent.parent.parent
# settings_file = os.environ.get("SETTINGS_FILE", "api.dev.yml")
# DEFAULT_CONFIG_PATH = PATH / "config" / settings_file
# with open(DEFAULT_CONFIG_PATH, "r") as ymlfile:
#     cfg = yaml.safe_load(ymlfile)

app = Celery(
    "celery_worker",
    
    broker=f'amqp://{config["rabbitmq"]["username"]}:{config["rabbitmq"]["password"]}@{config["rabbitmq"]["host"]}:{config["rabbitmq"]["port"]}',
    include=["celery_worker.tasks"],
)
# BASEDIR = "./"
app.conf.broker_transport_options = {
    "max_retries": 3,
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 0.2,
}
