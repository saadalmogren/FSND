"""empty message

Revision ID: f1dd5e513d14
Revises: 63b9a1c65340
Create Date: 2020-05-19 01:44:11.833007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1dd5e513d14'
down_revision = '63b9a1c65340'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'availability')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('availability', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###