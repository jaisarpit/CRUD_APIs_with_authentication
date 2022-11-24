"""create content column

Revision ID: 59c3c8198822
Revises: 5b8a418175cc
Create Date: 2022-11-22 19:18:42.390202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59c3c8198822'
down_revision = '5b8a418175cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
