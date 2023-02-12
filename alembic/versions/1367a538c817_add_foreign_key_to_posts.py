"""add foreign key to posts

Revision ID: 1367a538c817
Revises: 10b9b03f0590
Create Date: 2023-02-12 19:54:52.798177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1367a538c817'
down_revision = '10b9b03f0590'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass