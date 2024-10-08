from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class Price(BaseModel):

    product: Optional[int] = Field(alias='product')


class Stock(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    wh: int
    quantity: int = Field(alias='qty')


class Size(BaseModel):

    size: str = Field(alias='name')
    price: Optional[Price] = Field(exclude=True, default=None)
    quantity_by_wh: Optional[List[Stock]] = Field(alias='stocks', default=None)


class ProductSchema(BaseModel):

    nm_id: int = Field(alias='id')
    sum_quantity: int = Field(alias='totalQuantity')
    quantity_by_sizes: List[Size] = Field(alias='sizes')

    @computed_field
    @property
    def current_price(self) -> float:
        return self.quantity_by_sizes[0].price.product / 100


class StockResponse(BaseModel):

    wh: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class SizeResponse(BaseModel):

    size: str
    quantity_by_wh: List[StockResponse]

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):

    nm_id: int
    current_price: float
    sum_quantity: int
    quantity_by_sizes: List[SizeResponse]

    model_config = ConfigDict(from_attributes=True)
