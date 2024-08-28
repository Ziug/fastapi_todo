from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys

sys.path.append("..")

import schemas, models, oauth2
from database import get_db


router = APIRouter(prefix="/todo", tags=["todo"])


# ============================================ get ============================================
@router.get("")
async def get_all_user_todos(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_curr_usr)):
    return db.query(models.TodoTask).filter(models.TodoTask.user_id == current_user.id).all()


# ============================================ create ============================================
@router.post("", response_model=schemas.TodoTask)
async def create_todo_task(
    todo_task: schemas.TodoTask,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_curr_usr)
):
    print(type(todo_task.name))
    new_task = models.TodoTask(name=str(todo_task.name), user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
