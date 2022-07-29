"""Add users table

Revision ID: e8a49874e9c8
Revises: e337e2d594f2
Create Date: 2022-07-28 10:09:25.423672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8a49874e9c8'
down_revision = 'e337e2d594f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(), nullable=False),
                    sa.Column('email',sa.String(), nullable=False),
                    sa.Column('password',sa.String(), nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')                    
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
