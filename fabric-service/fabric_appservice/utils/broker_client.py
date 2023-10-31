import asyncio

import aio_pika
from aio_pika.pool import Pool
import json

from utils.logging import get_logger

_LOGGER = get_logger(__name__)


class BrokerClient:

    def __init__(self, username, password, host, port):
        _loop = asyncio.get_event_loop()
        self.__url = f"amqp://{username}:{password}@{host}:{port}"
        self.__connection_pool = Pool(self._get_connection,  max_size=2, loop=_loop)
        self.__channel_pool = Pool(self._get_channel, max_size=10, loop=_loop)

    async def _get_connection(self):
        return await aio_pika.connect_robust(self.__url)

    async def _get_channel(self) -> aio_pika.Channel:
        async with self.__connection_pool.acquire() as connection:
            return await connection.channel()

    async def close(self):
        await self.__channel_pool.close()
        await self.__connection_pool.close()

    async def consume(self, queue_name, event_handlers):
        async with self.__channel_pool.acquire() as channel:
            await channel.set_qos(10)

            exchange = await channel.declare_exchange(name="v-chain", type=aio_pika.ExchangeType.TOPIC, durable=True)

            queue = await channel.declare_queue(
                queue_name, durable=False, auto_delete=False
            )
            routing_keys = event_handlers.keys()
            for key in routing_keys:
                await queue.bind(exchange=exchange, routing_key=key)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    handler = event_handlers[message.routing_key]
                    body = json.loads(message.body.decode('utf-8'))
                    try:
                        await handler(body=body, reply_to=message.reply_to,
                                      message_id=message.message_id)
                    except Exception as e:
                        if hasattr(e, 'message'):
                            _LOGGER.exception(f'ERROR: {e.message}')
                        else:
                            _LOGGER.exception(f'ERROR: {e}')
                    await message.ack()

    async def publish(self, routing_key, message, reply_to=None):
        async with self.__channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(name="v-chain", type=aio_pika.ExchangeType.TOPIC, durable=True)
            await exchange.publish(
                aio_pika.Message(body=message.encode(), reply_to=reply_to),
                routing_key=routing_key,
            )
