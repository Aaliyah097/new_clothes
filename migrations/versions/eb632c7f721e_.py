"""empty message

Revision ID: eb632c7f721e
Revises: d4503515d044
Create Date: 2023-03-12 09:51:01.311687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb632c7f721e'
down_revision = 'd4503515d044'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'product', ['parent_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###