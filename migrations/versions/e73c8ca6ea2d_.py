"""empty message

Revision ID: e73c8ca6ea2d
Revises: eb632c7f721e
Create Date: 2023-03-12 23:18:01.487373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e73c8ca6ea2d'
down_revision = 'eb632c7f721e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Integer(),
               type_=postgresql.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)

    # ### end Alembic commands ###
