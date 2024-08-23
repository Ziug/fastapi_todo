from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    
class TodoTask(BaseModel):
    name: str

class TodoSubtask(TodoTask):
    ...