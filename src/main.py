from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import ORJSONResponse

from api.v1 import base
from core.config import app_settings
from core.taskiq import broker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    if not broker.is_worker_process:
        await broker.startup()

    yield

    if not broker.is_worker_process:
        await broker.shutdown()


app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)
app.include_router(base.api_router, prefix="/api/v1")

if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
    )
