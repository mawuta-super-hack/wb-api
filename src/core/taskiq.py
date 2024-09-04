from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import InMemoryBroker
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker

redis_async_result = RedisAsyncResultBackend(
 redis_url="redis://localhost:6379",
)

broker = ListQueueBroker(
 url="redis://localhost:6379").with_result_backend(redis_async_result)



scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)
