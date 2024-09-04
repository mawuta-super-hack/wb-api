class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
import datetime
from typing import Generic, Optional, Type, TypeVar
from aiogram.client.session.aiohttp import AiohttpSession
import asyncpg
from abc import ABC, abstractmethod
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import exc, select, exists, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
import requests
from schemas.product import ProductSchema, ProductResponse
from core.taskiq import broker
from db.db import get_session
from taskiq import TaskiqDepends
from core.taskiq import source
ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
from .parser import parse

from models.product import Product, Wh, Size

from task.api_task import create_task, update_task

class RepositoryDBProduct(Repository, Generic[ModelType, CreateSchemaType]):
    """CRUD class for File model."""

    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, nm_id: int) -> Optional[ModelType]:

        statement = select(Product).where(Product.nm_id == nm_id).exists()
        result = await db.scalar(select(statement))

        if result==True:
            join_statement = select(Product).options(
                joinedload(Product.quantity_by_sizes
                        ).options(joinedload(Size.quantity_by_wh))).where(Product.nm_id==nm_id)
            join_result = await db.execute(statement=join_statement)
            item = join_result.scalars().unique().one()
            return item
        else:
            try:
                data = await parse(nm_id)
                await create_task.kiq(obj_in=data)
                return data
            except IndexError:
                return None    
