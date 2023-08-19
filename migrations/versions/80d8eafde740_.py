"""empty message

Revision ID: 80d8eafde740
Revises: 03abe5900e35
Create Date: 2023-03-11 13:13:40.034292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80d8eafde740'
down_revision = '03abe5900e35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products_images',
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('product_image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['product_image_id'], ['product_image.id'], )
    )
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_constraint('product_image_id_fkey', type_='foreignkey')
        batch_op.drop_column('image_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('product_image_id_fkey', 'product_image', ['image_id'], ['id'])

    op.drop_table('products_images')
    # ### end Alembic commands ###
