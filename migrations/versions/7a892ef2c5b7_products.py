"""products

Revision ID: 7a892ef2c5b7
Revises: 5356fb411224
Create Date: 2023-03-09 20:10:35.313758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a892ef2c5b7'
down_revision = '5356fb411224'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_constraint('product_sku_key', type_='unique')
        batch_op.create_index(batch_op.f('ix_product_sku'), ['sku'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_sku'))
        batch_op.create_unique_constraint('product_sku_key', ['sku'])

    # ### end Alembic commands ###
