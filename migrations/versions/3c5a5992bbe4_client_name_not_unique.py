"""client_name_not_unique

Revision ID: 3c5a5992bbe4
Revises: df3b928cc391
Create Date: 2022-07-26 18:50:08.868043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c5a5992bbe4'
down_revision = 'df3b928cc391'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='fleet')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'fleet', ['name'], unique=False)
    # ### end Alembic commands ###
