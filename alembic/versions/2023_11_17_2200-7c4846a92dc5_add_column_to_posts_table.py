"""add column to posts table

Revision ID: 7c4846a92dc5
Revises: 97c0947689de
Create Date: 2023-11-17 22:00:29.053870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c4846a92dc5'
down_revision: Union[str, None] = '97c0947689de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('is_published', sa.Boolean(), default=False))


def downgrade() -> None:
    op.drop_column('posts', 'is_published')
