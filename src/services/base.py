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

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)

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
                        ).options(joinedload(Size.quantity_by_wh))).where(Product.nm_id == nm_id)
            join_result = await db.execute(statement=join_statement)
            item = join_result.scalars().unique().one()
            #return item
        else:
            data = await self.parse(nm_id)
            print(data)
            # типа передаем в очередь создание в бд
            await create_task.kiq(obj_in=data)
        await self.update_task(db)
        #return data
        
    async def parse(self, id):
        response = requests.get(
        f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-5818883&spp=30&ab_testing=false&nm={id}')
        item = ProductSchema.model_validate(response.json()['data']['products'][0]).model_dump(by_alias=False)
        return item
    

    async def update_task(self, db: AsyncSession) -> None:
        print('##### UPDATE TASK')
        products = await db.execute(select(Product))

        for product in products.scalars().all():
            new_data = await self.parse(product.nm_id)
            p =  ProductSchema.model_validate(new_data)

            product.current_price = new_data['current_price']
            product.sum_quantity = new_data['sum_quantity']

            # sizes_list = new_data.pop('quantity_by_sizes')
            # sizes = await db.execute(select(Size).where(Size.product_id==product.nm_id))
            # print(sizes)
            # #for obj_size in sizes.scalars().all():
            # for size_new in sizes_list:
            #     if size_new['size'] == 


            #for size in sizes_list:
                #warehouses_list = size.pop('quantity_by_wh')
                #await db.execute(delete(Wh).where(Wh.size_id == size.id))

            #     for wh in warehouses_list:
            #         wb_object = Wh(**wh)
            #         wb_object.size_id = size.id
            #         db.add(wb_object)
            #         await db.commit()
            # await db.refresh(product)

                    #связывкамся через размер и удаляем то что есть




# @broker.task
# async def create_task(obj_in: CreateSchemaType, db: AsyncSession = TaskiqDepends(get_session)) -> None:
#     #print('################################', db=db['dependancy'], obj_in)
#     #db=db['dependancy']
#     print('################################', obj_in)
#     obj_in_data = jsonable_encoder(obj_in)
#     prod_id = obj_in_data['nm_id']
#     sizes = obj_in_data.pop('quantity_by_sizes')

#     db_obj = Product(**obj_in_data)
#     db.add(db_obj)
#     await db.commit()
#     await db.refresh(db_obj)

#     for s in sizes:
#         obj = Size(size=s['size'], product_id=prod_id)
#         db.add(obj)
#         await db.commit()
#         await db.refresh(db_obj)
#         whs = s.pop('quantity_by_wh')
#         if whs == []:
#             continue
        
#         for w in whs:
#             ob = Wh(**w)
#             ob.size_id = obj.id
#             db.add(ob)
#             await db.commit()
#             await db.refresh(db_obj)

    #await db.refresh(db_obj)

# async def parse(self, id):
#     response = requests.get(
#     f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-5818883&spp=30&ab_testing=false&nm={id}')
#     item = ProductSchema.model_validate(response.json()['data']['products'][0]).model_dump(by_alias=False)
    
#     return item
