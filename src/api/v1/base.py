from .product import router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(router, prefix="/product", tags=["product"])