from fastapi import FastAPI
from routes.autheticationRoute import authRouter
from routes.taskRoute import task_router

app = FastAPI()
app.include_router(authRouter, prefix="/auth", tags = ["Authentication"])