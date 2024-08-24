from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

class TodoTask(BaseModel):
    name: str
    user: int

class TodoSubtask(TodoTask):
    ...
    
class TokenData(BaseModel):
    id: Optional[str] = None