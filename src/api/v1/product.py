from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.product import *
from db.db import get_session
from services.product import product_crud
from schemas.product import *
from schemas.product import ProductSchema, ProductResponse
router = APIRouter()


@router.get("/{nm_id}", response_model=ProductResponse)
async def read_entity(
    *,
    db: AsyncSession = Depends(get_session),
    nm_id: int,
) -> Any:
    """
    Get by ID.
    """
    # get entity from db
    entity = await product_crud.get(db=db, nm_id=nm_id)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return entity
