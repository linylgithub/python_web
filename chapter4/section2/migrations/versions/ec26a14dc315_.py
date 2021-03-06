"""empty message

Revision ID: ec26a14dc315
Revises: 47298f68f7af
Create Date: 2018-11-24 16:54:30.808445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec26a14dc315'
down_revision = '47298f68f7af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('login_users', sa.Column('email', sa.String(length=128), nullable=False))
    op.add_column('login_users', sa.Column('password', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('login_users', 'password')
    op.drop_column('login_users', 'email')
    # ### end Alembic commands ###
