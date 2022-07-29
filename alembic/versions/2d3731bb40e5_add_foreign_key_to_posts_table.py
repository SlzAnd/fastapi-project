"""Add foreign-key to posts table

Revision ID: 2d3731bb40e5
Revises: e8a49874e9c8
Create Date: 2022-07-28 10:23:26.542737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d3731bb40e5'
down_revision = 'e8a49874e9c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False)
                  )
    op.create_foreign_key('post_user_fk',source_table='posts', referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'], ondelete="CASCADE"
                          )
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
