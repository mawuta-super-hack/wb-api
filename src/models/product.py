from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Product(Base):
    __tablename__ = 'product'

    nm_id: Mapped[int] = mapped_column(primary_key=True)
    current_price: Mapped[float]
    sum_quantity: Mapped[int]
    quantity_by_sizes: Mapped[List['Size']] = relationship(
        back_populates='product',
        cascade='save-update, merge, delete, delete-orphan'
    )


class Size(Base):
    __tablename__ = 'size'

    id: Mapped[int] = mapped_column(primary_key=True)
    size: Mapped[str] = mapped_column(String(30))

    quantity_by_wh: Mapped[List['Wh']] = relationship(
        back_populates='size',
        cascade='save-update, merge, delete, delete-orphan'
    )

    product_id: Mapped[int] = mapped_column(ForeignKey('product.nm_id'))
    product: Mapped['Product'] = relationship(
        back_populates='quantity_by_sizes'
    )


class Wh(Base):
    __tablename__ = 'wh'

    id: Mapped[int] = mapped_column(primary_key=True)
    wh: Mapped[int]
    quantity: Mapped[int]

    size_id: Mapped[int] = mapped_column(ForeignKey('size.id'))
    size: Mapped['Size'] = relationship(back_populates='quantity_by_wh')
