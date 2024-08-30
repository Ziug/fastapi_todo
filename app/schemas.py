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
    is_done: bool = False


class TodoSubtaskOut(TodoSubtask):
    id: int

    class Config:
        orm_mode = True


class TodoTask(BaseModel):
    name: str | int


class TodoTaskOut(TodoTask):
    id: int
    progress: float 
    subtasks: List["TodoSubtaskOut"]

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[int] = None


class Token(BaseModel):
    access_token: str
    token_type: str
