from typing import List, Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    
    class Config:
        orm_mode = True

class TodoSubtask(BaseModel):
    name: str | int
    task_id: int
    is_done: bool = False

class TodoTask(BaseModel):
    name: str | int
    subtasks: List["TodoSubtask"] = []

class TodoTaskOut(TodoTask):
    id: int
    
    class Config:
        orm_mode = True
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class Token(BaseModel):
    access_token: str
    token_type: str