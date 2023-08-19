"""empty message

Revision ID: bd24f0e8cc2a
Revises: 003176900687
Create Date: 2023-03-12 08:36:16.308989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd24f0e8cc2a'
down_revision = '003176900687'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('color_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('size_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'size', ['size_id'], ['id'])
        batch_op.create_foreign_key(None, 'color', ['color_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('size_id')
        batch_op.drop_column('color_id')

    # ### end Alembic commands ###