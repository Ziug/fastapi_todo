from turtle import st
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys

sys.path.append("..")

import schemas, models, oauth2
from database import get_db


router = APIRouter(prefix="/todo", tags=["todo"])


# ============================================ get ============================================
@router.get("", response_model=List[schemas.TodoTaskOut])
async def get_all_user_todos(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_curr_usr)):
    return db.query(models.TodoTask).filter(models.TodoTask.user_id == current_user.id).all()


# ============================================ create ============================================
@router.post("", response_model=schemas.TodoTask)
async def create_todo_task(
    todo_task: schemas.TodoTask,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_curr_usr)
):
    new_task = models.TodoTask(name=str(todo_task.name), user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.post("/{id}", response_model=schemas.TodoSubtask)
async def create_todo_subtask(todo_subtask: schemas.TodoSubtask,
                              id: int,
                              db: Session = Depends(get_db),
                              current_user: models.User = Depends(oauth2.get_curr_usr)):
    
    task = db.query(models.TodoTask).filter(models.TodoTask.id == id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task №{id} not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You don't have permission to create a subtask for task №{id}")
    
    new_subtask = models.TodoSubtask(name=todo_subtask.name, task_id=id)
    print(new_subtask)
    
    db.add(new_subtask)
    db.commit()
    db.refresh(new_subtask)
    
    return new_subtask
    

# ============================================ update ============================================



# ============================================ delete ============================================
@router.delete('/{id}')
async def delete_todo_task(id: int,
                           db: Session = Depends(get_db),
                           current_user: models.User = Depends(oauth2.get_curr_usr)):
    
    task = db.query(models.TodoTask).filter(models.TodoTask.id == id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task №{id} not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You don't have permission to delete task №{id}")
    
    db.delete(task)
    db.commit()
    
    return {"message": f"Task №{id} was deleted"}