import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import base
from core.config import app_settings
from core.taskid import broker
from fastapi.concurrency import asynccontextmanager
from typing import AsyncIterator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    # Запуск TaskIQ брокера, если это не процесс выполнения задачи
    if not broker.is_worker_process:
        await broker.startup()
    yield
    # Завершение работы TaskIQ брокера при остановке приложения
    # if not broker.is_worker_process:
    #     await broker.shutdown()


app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse, 
    lifespan=lifespan
)
app.include_router(base.api_router, prefix="/api/v1")

if __name__ == '__main__':
       # `uvicorn main:app --host 0.0.0.0 --port 8080 --app-dir src`
       #uvicorn main:app --host 127.0.0.1 --port 8080 --reload
       #uvicorn main:app --reload 
       #taskiq scheduler core.taskid:scheduler
       #taskiq worker core.taskid:broker --workers=2 --log-level=INFO
       #taskiq worker core.taskid:broker task.task


    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
    )