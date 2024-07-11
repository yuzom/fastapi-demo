"""add content column to posts table

Revision ID: a6fac9766af2
Revises: ce62a15381f8
Create Date: 2024-07-11 13:29:33.930828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6fac9766af2'
down_revision: Union[str, None] = 'ce62a15381f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
