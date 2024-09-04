
from core.taskiq import broker
from db.db import get_session
from taskiq import TaskiqDepends
from models.product import Product, Wh, Size
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select
from fastapi.encoders import jsonable_encoder
from services.parser import parse


@broker.task
async def create_task(obj_in: dict, db: AsyncSession = TaskiqDepends(get_session)) -> None:

    obj_in_data = jsonable_encoder(obj_in)
    prod_id = obj_in_data['nm_id']
    sizes = obj_in_data.pop('quantity_by_sizes')

    db_obj = Product(**obj_in_data)
    db.add(db_obj)
    await db.commit()

    for s in sizes:
        obj = Size(size=s['size'], product_id=prod_id)
        db.add(obj)
        await db.commit()
        
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
    products = await db.execute(select(Product))

    for product in products.scalars().all():
        new_data = await parse(product.nm_id)
                
        old_product = await db.scalar(select(Product).where(Product.nm_id==product.nm_id))
        await db.delete(old_product)
        await db.commit()

        await create_task.kiq(obj_in=new_data)
