from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import InMemoryBroker
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker, RedisScheduleSource
from dotenv import load_dotenv
from os import getenv
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
