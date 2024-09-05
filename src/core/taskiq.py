from os import getenv

from dotenv import load_dotenv
from taskiq import TaskiqScheduler
from taskiq_redis import (ListQueueBroker, RedisAsyncResultBackend,
                          RedisScheduleSource)

load_dotenv()


redis_async_result = RedisAsyncResultBackend(
 redis_url=getenv('REDIS'),
)

broker = ListQueueBroker(
 url=getenv('REDIS')).with_result_backend(redis_async_result)


source = RedisScheduleSource(getenv('REDIS'))


scheduler = TaskiqScheduler(
    broker=broker,
    sources=[source],
)
