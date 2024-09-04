
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from core.taskid import broker
from db.db import get_session
from taskiq import TaskiqDepends
from models.product import Product, Wh, Size
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select
from fastapi.encoders import jsonable_encoder
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)

@broker.task
async def create_task(obj_in: dict, db: AsyncSession = TaskiqDepends(get_session)) -> None:

    obj_in_data = jsonable_encoder(obj_in)
    prod_id = obj_in_data['nm_id']
    sizes = obj_in_data.pop('quantity_by_sizes')

    db_obj = Product(**obj_in_data)
    db.add(db_obj)
    await db.commit()
    #await db.refresh(db_obj)

    for s in sizes:
        obj = Size(size=s['size'], product_id=prod_id)
        db.add(obj)
        await db.commit()
        #await db.refresh(db_obj)
        whs = s.pop('quantity_by_wh')
        if whs == []:
            continue
        
        for w in whs:
            ob = Wh(**w)
            ob.size_id = obj.id
            db.add(ob)
            await db.commit()
    await db.refresh(db_obj)

@broker.task(schedule=[{"cron": "*/5 * * * *"}])
async def update_task(db: AsyncSession = TaskiqDepends(get_session)) -> None:
    print('##### UPDATE TASK')
    #obj_in_data = jsonable_encoder(obj_in)
    products = db.execute(select(Product))

    print(products.all())
    
    # prod_id = obj_in_data['nm_id']
    # sizes = obj_in_data.pop('quantity_by_sizes')

    # db_obj = Product(**obj_in_data)
    # db.add(db_obj)
    # await db.commit()
    # #await db.refresh(db_obj)

    # for s in sizes:
    #     obj = Size(size=s['size'], product_id=prod_id)
    #     db.add(obj)
    #     await db.commit()
    #     #await db.refresh(db_obj)
    #     whs = s.pop('quantity_by_wh')
    #     if whs == []:
    #         continue
        
    #     for w in whs:
    #         ob = Wh(**w)
    #         ob.size_id = obj.id
    #         db.add(ob)
    #         await db.commit()
    # await db.refresh(db_obj)