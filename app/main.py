from fastapi import FastAPI
from app.routers.auth import router
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/api/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app")