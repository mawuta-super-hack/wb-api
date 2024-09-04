"""01_initial.

Revision ID: 07bbd1d8a0e3
Revises: 
Create Date: 2024-09-03 16:20:18.317512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07bbd1d8a0e3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('nm_id', sa.Integer(), nullable=False),
    sa.Column('current_price', sa.Float(), nullable=False),
    sa.Column('sum_quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('nm_id')
    )
    op.create_table('size',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('size', sa.String(length=30), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.nm_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wh',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wh', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('size_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['size_id'], ['size.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wh')
    op.drop_table('size')
    op.drop_table('product')
    # ### end Alembic commands ###
