from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, String, Float, ForeignKey, text)


# fastapi + sqlalchemy models for ToDo app
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class TodoTask(Base):
    __tablename__ = "todo_task"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, server_default=text("ToDo task name"))
    progress = Column(Float, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("now()"))
    user_id = Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))
    subtasks = relationship("TodoSubtask")


class TodoSubtask(Base):
    __tablename__ = "todo_subtask"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    is_done = Column(Boolean, default=False)
    task_id = Column("task_id", Integer, ForeignKey("todo_task.id", ondelete="CASCADE"))