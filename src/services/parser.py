import requests
from pydantic import BaseModel, Field, root_validator, model_validator, field_validator, validator, computed_field
from typing import List, Optional, Annotated


class Price(BaseModel):
   price: int = Field(alias='product')
 
class Stock(BaseModel):
    wh: int
    quantity: int = Field(alias='qty')

class Size(BaseModel):
    size: str =Field(alias='name')
    price: Price =Field(exclude=True)
    quantity_by_wh: List[Stock] = Field(alias='stocks')

class Product(BaseModel):
    nm_id: int= Field(alias='id')
    # price: Size.price
    #current_price: computed_field
    
    

    @computed_field
    @property
    def current_price(self) -> float:
        return self.quantity_by_sizes[0].price.price / 100

    sum_quantity: int = Field(alias='totalQuantity')
    quantity_by_sizes: List[Size] = Field(alias='sizes')

class ProductModel(BaseModel):
    nm_id: int= Field(alias='id')
    current_price:float
    sum_quantity: int = Field(alias='totalQuantity')
    quantity_by_sizes: List[Size] = Field(alias='sizes')


    # @field_validator('price')
    # @classmethod
    # def product(cls, value):
    #     value = cls.quantity_by_sizes[0].price.current_price / 100
    #     print(value)
    #     return value

    
# class Items(BaseModel):
#     products: List[Product]


class Parser():
    def __init__(self, id: str):
        self.product_id = id

    # def __get_product_id(self, url: str):
    #     regex = '(?<=catalog/).+(?=/detail)'
    #     product_id = re.search(regex, url)
    #     return product_id
    
    def parse(self):
        response = requests.get(
        f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-5818883&spp=30&ab_testing=false&nm={self.product_id}')
        
        
        item = Product.parse_obj(response.json()['data']['products'][0])
        print(item.dict())

    

Parser('142054897').parse()