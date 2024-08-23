from fastapi import FastAPI
import uvicorn


from routers import todo, users

app = FastAPI()

@app.get('/')
async def home_page():
    return {'message':'Hello World!'}

app.include_router(todo.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)