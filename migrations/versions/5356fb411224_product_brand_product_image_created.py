"""product, brand, product_image created

Revision ID: 5356fb411224
Revises: 
Create Date: 2023-03-09 19:52:47.173005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5356fb411224'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('logo__mime_type', sa.String(length=1015), nullable=True),
    sa.Column('logo__ext', sa.String(length=1009), nullable=True),
    sa.Column('logo__file_name', sa.String(length=1015), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.Column('sku', sa.String(length=10), nullable=False),
    sa.Column('mark', sa.String(length=20), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price_old', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sku')
    )
    op.create_table('product_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('image__mime_type', sa.String(length=1016), nullable=True),
    sa.Column('image__ext', sa.String(length=1010), nullable=True),
    sa.Column('image__file_name', sa.String(length=1016), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_image')
    op.drop_table('product')
    op.drop_table('category')
    op.drop_table('brand')
    # ### end Alembic commands ###
