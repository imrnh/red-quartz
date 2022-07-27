from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from database.schemas import Settings
from routes.autheticationRoute import authRouter
from routes.taskRoute import task_router

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(authRouter, prefix="/auth", tags = ["Authentication"])