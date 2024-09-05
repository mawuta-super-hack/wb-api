
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from core.taskiq import broker
from db.db import get_session
from models.product import Product, Size, Wh
from services.parser import parse


@broker.task
async def create_task(
    obj_in: dict,
    db: AsyncSession = TaskiqDepends(get_session)
) -> None:

    parse_data = jsonable_encoder(obj_in)
    product_id = parse_data['nm_id']
    quantity_by_sizes = parse_data.pop('quantity_by_sizes')

    db_product = Product(**parse_data)
    db.add(db_product)
    await db.commit()

    for size in quantity_by_sizes:
        db_size = Size(size=size['size'], product_id=product_id)
        db.add(db_size)
        await db.commit()
        warehouses = size.pop('quantity_by_wh')

        if warehouses == []:
            continue
        for wh in warehouses:
            db_wh = Wh(**wh)
            db_wh.size_id = db_size.id
            db.add(db_wh)
            await db.commit()
    await db.refresh(db_product)


@broker.task(schedule=[{'cron': '*/5 * * * *'}])
async def update_task(db: AsyncSession = TaskiqDepends(get_session)) -> None:
    products = await db.execute(select(Product))

    for product in products.scalars().all():
        new_data = await parse(product.nm_id)

        old_product = await db.scalar(select(Product).where(
            Product.nm_id == product.nm_id)
        )
        await db.delete(old_product)
        await db.commit()

        await create_task.kiq(obj_in=new_data)
