from celery import Celery

from settings import config as cfg

app = Celery(
    "worker",
    broker="amqp://{}:{}@{}:{}".format(cfg["rabbitmq"]["username"],
                                       cfg["rabbitmq"]["password"],
                                       cfg["rabbitmq"]["host"],
                                       cfg["rabbitmq"]["port"]),
    include=["worker.tasks"],
)

app.conf.broker_transport_options = {
    "max_retries": 3,
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 0.2,
}

app.conf.task_default_queue = 'sawtooth.tasks'
app.conf.task_default_exchange = 'sawtooth.tasks'
app.conf.task_default_exchange_type = 'topic'
app.conf.task_default_routing_key = 'sawtooth.tasks'