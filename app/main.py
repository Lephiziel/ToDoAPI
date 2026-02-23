from fastapi import FastAPI
from app.routers.auth import router
from app.routers.todos import todo_router
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/api/auth", tags=["auth"])

app.include_router(todo_router, prefix="/api/todos", tags=["todos"])

if __name__ == "__main__":
    uvicorn.run("main:app")