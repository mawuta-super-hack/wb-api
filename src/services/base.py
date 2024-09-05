
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.product import Product, Size
from task.api_task import create_task

from .parser import parse


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDBProduct(Repository):

    async def get(self, db: AsyncSession, nm_id: int) -> Any:
        statement = select(Product).where(Product.nm_id == nm_id).exists()
        result = await db.scalar(select(statement))
        if result:
            join_statement = select(Product).options(
                joinedload(
                    Product.quantity_by_sizes
                ).options(joinedload(Size.quantity_by_wh))).where(
                    Product.nm_id == nm_id
                )
            join_result = await db.execute(statement=join_statement)
            product = join_result.scalars().unique().one()
            return product
        else:
            try:
                data = await parse(nm_id)
                await create_task.kiq(obj_in=data)
                return data
            except IndexError:
                return None
