"""add content column

Revision ID: e337e2d594f2
Revises: 5e3025428f58
Create Date: 2022-07-28 09:59:47.590299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e337e2d594f2'
down_revision = '5e3025428f58'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
