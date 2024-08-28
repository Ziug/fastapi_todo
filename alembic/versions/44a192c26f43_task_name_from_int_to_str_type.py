"""task name from int to str type

Revision ID: 44a192c26f43
Revises: be5006122a0e
Create Date: 2024-08-25 23:15:33.415950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44a192c26f43'
down_revision: Union[str, None] = 'be5006122a0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("todo_task", "name", type_=sa.String)
    pass


def downgrade() -> None:
    op.alter_column("todo_task", "name", type_=sa.Integer)
    pass
