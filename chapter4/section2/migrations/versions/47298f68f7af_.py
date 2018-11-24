"""empty message

Revision ID: 47298f68f7af
Revises: 4ab575e3b6b9
Create Date: 2018-11-24 16:53:39.113053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47298f68f7af'
down_revision = '4ab575e3b6b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login_users')
    # ### end Alembic commands ###