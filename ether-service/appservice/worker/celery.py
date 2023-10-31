from celery import Celery

from settings import config as cfg

app = Celery(
    "worker",
    broker="amqp://"
    + cfg["rabbitmq"]["username"]
    + ":"
    + cfg["rabbitmq"]["password"]
    + "@"
    + cfg["rabbitmq"]["host"]
    + ":5672//",
    include=["worker.tasks"],
)

app.conf.broker_transport_options = {
    "max_retries": 3,
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 0.2,
}
