"""empty message

Revision ID: e4b345cd3adf
Revises: b7e39498ba88
Create Date: 2023-03-10 12:13:13.456047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4b345cd3adf'
down_revision = 'b7e39498ba88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand', schema=None) as batch_op:
        batch_op.alter_column('type',
               existing_type=sa.VARCHAR(length=3),
               type_=sa.Unicode(length=4),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand', schema=None) as batch_op:
        batch_op.alter_column('type',
               existing_type=sa.Unicode(length=4),
               type_=sa.VARCHAR(length=3),
               existing_nullable=True)

    # ### end Alembic commands ###
