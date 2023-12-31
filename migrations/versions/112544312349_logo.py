"""logo

Revision ID: 112544312349
Revises: 7a892ef2c5b7
Create Date: 2023-03-09 21:27:28.771123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '112544312349'
down_revision = '7a892ef2c5b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand', schema=None) as batch_op:
        batch_op.drop_column('logo__ext')
        batch_op.drop_column('logo__mime_type')
        batch_op.drop_column('logo__file_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand', schema=None) as batch_op:
        batch_op.add_column(sa.Column('logo__file_name', sa.VARCHAR(length=1015), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('logo__mime_type', sa.VARCHAR(length=1015), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('logo__ext', sa.VARCHAR(length=1009), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
