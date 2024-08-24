from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys

sys.path.append("..")

import oauth2
import schemas
from models import TodoTask, User
from database import get_db


router = APIRouter(prefix="/todo", tags=["todo"])


# ============================================ get ============================================
@router.get("")
async def get_all(db: Session = Depends(get_db)):
    return db.query(TodoTask).all()


# ============================================ create ============================================
@router.post("")
async def create_todo_task(
    todo_task: schemas.TodoTask,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    new_task = TodoTask(name=todo_task.name, user=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
