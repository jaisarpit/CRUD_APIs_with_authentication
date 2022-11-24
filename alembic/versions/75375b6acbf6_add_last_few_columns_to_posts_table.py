"""add last few columns to posts table

Revision ID: 75375b6acbf6
Revises: cba057387914
Create Date: 2022-11-24 13:28:32.409285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75375b6acbf6'
down_revision = 'cba057387914'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default= sa.text('now()'), 
    nullable=False),)
        
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
