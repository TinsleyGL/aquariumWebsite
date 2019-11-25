"""extend aquarium table

Revision ID: bb56708fcf4f
Revises: 03d46ae954e1
Create Date: 2019-11-23 11:24:10.777606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb56708fcf4f'
down_revision = '03d46ae954e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('aquarium', sa.Column('targetClarity', sa.Integer(), nullable=True))
    op.add_column('aquarium', sa.Column('targetPH', sa.Integer(), nullable=True))
    op.add_column('aquarium', sa.Column('targetTemperature', sa.Integer(), nullable=True))
    op.add_column('aquarium', sa.Column('targetWaterflow', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('aquarium', 'targetWaterflow')
    op.drop_column('aquarium', 'targetTemperature')
    op.drop_column('aquarium', 'targetPH')
    op.drop_column('aquarium', 'targetClarity')
    # ### end Alembic commands ###
