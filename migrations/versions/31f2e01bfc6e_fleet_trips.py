"""fleet_trips

Revision ID: 31f2e01bfc6e
Revises: 3c5a5992bbe4
Create Date: 2022-07-26 20:35:30.644577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31f2e01bfc6e'
down_revision = '3c5a5992bbe4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trip', sa.Column('fleet_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'trip', 'fleet', ['fleet_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trip', type_='foreignkey')
    op.drop_column('trip', 'fleet_id')
    # ### end Alembic commands ###
