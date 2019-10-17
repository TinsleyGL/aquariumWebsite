"""updated post

Revision ID: 583e8bb34dfe
Revises: 5d38427057c7
Create Date: 2019-10-05 13:51:49.711649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '583e8bb34dfe'
down_revision = '5d38427057c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('aquarium', 'ph')
    op.drop_column('aquarium', 'temperature')
    op.add_column('post', sa.Column('image_filename', sa.String(), nullable=True))
    op.add_column('post', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'image_url')
    op.drop_column('post', 'image_filename')
    op.add_column('aquarium', sa.Column('temperature', sa.INTEGER(), nullable=True))
    op.add_column('aquarium', sa.Column('ph', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###