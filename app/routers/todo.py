from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Integer, cast, func
from sqlalchemy.orm import Session
import sys

sys.path.append("..")

import schemas, models, oauth2
from database import get_db


router = APIRouter(prefix="/todo", tags=["todo"])


async def check_if_exists(task, id: int, user_id: int, sub = None, sub_id: int = None, db: Session = Depends(get_db)):
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task №{id} not found")
    
    if task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You don't have permission to access task №{id}")
        
    if sub == None and sub_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Subtask №{sub_id} not found")
    
    if sub and sub.task_id != id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task №{id} has no subtask with id {sub_id}")
    
        

# ============================================ get ============================================
@router.get("", response_model=List[schemas.TodoTaskOut])
async def get_all_user_todos(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_curr_usr)):
    return db.query(models.TodoTask).filter(models.TodoTask.user_id == current_user.id).all()


# ============================================ create ============================================
@router.post("", response_model=schemas.TodoTaskOut)
async def create_todo_task(
    todo_task: schemas.TodoTask,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_curr_usr)
):
    new_task = models.TodoTask(name=todo_task.name, user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.post("/{id}", response_model=schemas.TodoSubtaskOut)
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
@router.put("/{id}", response_model=schemas.TodoTaskOut)
async def update_todo_task(updated_task: schemas.TodoTask,
                           id: int,
                           db: Session = Depends(get_db),
                           current_user: models.User = Depends(oauth2.get_curr_usr)):
    
    task = db.query(models.TodoTask).filter(models.TodoTask.id == id)
    
    await check_if_exists(task=task.first(), id=id, user_id=current_user.id)
    
    task.update(updated_task.model_dump(), synchronize_session=False)
    db.commit()
    
    return task.first()

@router.put("/{id}/{sub_id}", response_model=schemas.TodoSubtaskOut)
async def update_todo_subtask(updated_subtask: schemas.TodoSubtask,
                              id: int,
                              sub_id: int,
                              db: Session = Depends(get_db),
                              current_user: models.User = Depends(oauth2.get_curr_usr)):
    
    task = db.query(models.TodoTask).filter(models.TodoTask.id == id).first()
    subtask = db.query(models.TodoSubtask).filter(models.TodoSubtask.id == sub_id)
    
    await check_if_exists(task=task, id=id, user_id=current_user.id, sub=subtask.first(), sub_id=sub_id)
    
    subtask.update(updated_subtask.model_dump(), synchronize_session=False)
    db.commit()
    
    return subtask.first()


# ============================================ delete ============================================
@router.delete('/{id}')
async def delete_todo_task(id: int,
                           db: Session = Depends(get_db),
                           current_user: models.User = Depends(oauth2.get_curr_usr)):
    
    task = db.query(models.TodoTask).filter(models.TodoTask.id == id)
    
    await check_if_exists(task=task.first(), id=id, user_id=current_user.id)
    
    task.delete(synchronize_session=False)
    db.commit()
    
    return {"message": f"Task №{id} was deleted"}


@router.delete('/{id}/{sub_id}')
async def delete_todo_subtask(id: int,
                              sub_id: int,
                              db: Session = Depends(get_db),
                              current_user: models.User = Depends(oauth2.get_curr_usr)):
    
    
    subtask = db.query(models.TodoSubtask).filter(models.TodoSubtask.id == sub_id)
    task = db.query(models.TodoTask).filter(models.TodoTask.id == id).first()
    
    await check_if_exists(task=task, id=id, user_id=current_user.id, sub=subtask.first(), sub_id=sub_id)
    
    subtask.delete(synchronize_session=False)
    db.commit()
    
    return {"message": f"Subtask №{sub_id} for task №{id} was deleted"}