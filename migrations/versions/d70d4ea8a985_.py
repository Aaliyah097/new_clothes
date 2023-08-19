"""empty message

Revision ID: d70d4ea8a985
Revises: 80d8eafde740
Create Date: 2023-03-11 14:38:29.835744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd70d4ea8a985'
down_revision = '80d8eafde740'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('sku',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=12),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('sku',
               existing_type=sa.String(length=12),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)

    # ### end Alembic commands ###