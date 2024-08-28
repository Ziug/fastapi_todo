"""add models: todo list/task, user

Revision ID: 66f5f3a49cc7
Revises: 
Create Date: 2024-08-23 16:24:55.877142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66f5f3a49cc7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String, nullable=False)
    )
    
    op.create_table(
        "todo_task",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String),
        sa.Column("progress", sa.Float),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), nullable=False, server_default=sa.text('now()')),
        sa.Column("user_id", sa.Integer, nullable = False)
    )
    
    op.create_foreign_key("task_users_fk", source_table="todo_task", referent_table="users",
                          local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    
    op.create_table(
        "todo_subtask",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("is_done", sa.Boolean, default=False),
        sa.Column("task_id", sa.Integer, nullable = False)
    )
    
    op.create_foreign_key("subtask_task_fk", source_table="todo_subtask", referent_table="todo_task",
                          local_cols=["task_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_table("todo_subtask")
    op.drop_table("todo_task")
    op.drop_table("users")
    pass
