from fastapi import Depends, FastAPI
import uvicorn


from models import User
from routers import todo, users, auth

app = FastAPI()


@app.get('/')
async def home_page():
    return {'message':'Hello World!'}

app.include_router(todo.router)
app.include_router(users.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    