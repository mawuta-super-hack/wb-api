from models.product import Product
from schemas.product import  ProductSchema

from .base import RepositoryDBProduct


class RepositoryProduct(RepositoryDBProduct[ProductSchema, Product  ]):
    pass


product_crud = RepositoryProduct(Product)