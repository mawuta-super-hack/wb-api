from fastapi import APIRouter

from .product import router

api_router = APIRouter()
api_router.include_router(router, prefix='/product', tags=['product'])
