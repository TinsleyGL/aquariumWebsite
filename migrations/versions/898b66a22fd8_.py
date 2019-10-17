"""empty message

Revision ID: 898b66a22fd8
Revises: 536cb9080a94
Create Date: 2019-10-17 19:54:04.010290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '898b66a22fd8'
down_revision = '536cb9080a94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image_filename', sa.String(), nullable=True))
    op.add_column('user', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image_url')
    op.drop_column('user', 'image_filename')
    # ### end Alembic commands ###