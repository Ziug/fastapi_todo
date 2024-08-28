"""make_usernames_unique

Revision ID: be5006122a0e
Revises: 66f5f3a49cc7
Create Date: 2024-08-25 22:41:57.891681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be5006122a0e'
down_revision: Union[str, None] = '66f5f3a49cc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uq_username', 'users',['username'])
    pass


def downgrade() -> None:
    op.drop_constraint("uq_username", "users")
    pass
