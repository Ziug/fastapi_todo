from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

class TodoTask(BaseModel):
    name: str | int

class TodoSubtask(TodoTask):
    ...
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class Token(BaseModel):
    access_token: str
    token_type: str