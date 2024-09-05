from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.product import ProductResponse
from services.product import product_crud

router = APIRouter()


@router.get('/{nm_id}', response_model=ProductResponse)
async def read_product(
    *,
    db: AsyncSession = Depends(get_session),
    nm_id: int,
) -> Any:
    product = await product_crud.get(db=db, nm_id=nm_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Товар не найден.'
        )
    return product
