from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from typing import List
class Product(Base):
    __tablename__ = 'product'


    nm_id: Mapped[int] = mapped_column(primary_key=True)
    current_price: Mapped[float]
    sum_quantity: Mapped[int]
    quantity_by_sizes: Mapped[List['Size']] = relationship(
        back_populates='product', cascade='save-update, merge, delete, delete-orphan'
    )


    

class Size(Base):
    __tablename__ = 'size'

    id: Mapped[int] = mapped_column(primary_key=True)
    size: Mapped[str] = mapped_column(String(30))

    quantity_by_wh: Mapped[List['Wh']] = relationship(
        back_populates='size', cascade='save-update, merge, delete, delete-orphan')

    product_id: Mapped[int] = mapped_column(ForeignKey('product.nm_id'))
    product: Mapped['Product'] = relationship(back_populates='quantity_by_sizes')



class Wh(Base):
    __tablename__ = 'wh'

    id: Mapped[int] = mapped_column(primary_key=True)
    wh: Mapped[int]
    quantity: Mapped[int]

    size_id: Mapped[int] = mapped_column(ForeignKey('size.id'))
    size: Mapped['Size'] = relationship(back_populates='quantity_by_wh')


