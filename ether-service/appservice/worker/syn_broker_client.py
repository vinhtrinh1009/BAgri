from kombu import Connection, Producer
import json
from config.logging_config import get_logger


_LOGGER = get_logger(__name__)


class BrokerClientSyn:
    def __init__(self, username, password, host, port):
        broker_url = f"amqp://{username}:{password}@{host}:{port}"
        self.rabbitmq_connection = Connection(broker_url)

    def publish_messages(self, message, routing_key):
        _LOGGER.debug("Publish message: {}".format(message))
        self.rabbitmq_connection.ensure_connection()
        try:
            with Producer(self.rabbitmq_connection) as producer:
                producer.publish(
                    json.dumps(message),
                    exchange="v-chain",
                    routing_key=routing_key,
                    retry=True
                )
        except:
            _LOGGER.debug(f"Cannot publish message with routing_key: {routing_key}")
