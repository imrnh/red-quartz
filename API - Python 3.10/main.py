from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from database.schemas import Settings

from routes.autheticationRoute import authRouter
from routes.taskCategoryRoute import task_category_router
from routes.taskRoute import task_router
from routes.pointsRoute import point_route

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(authRouter, prefix="/auth", tags = ["Authentication"])
app.include_router(task_category_router, prefix="/task_category", tags= ["Task Category"])
app.include_router(task_router, prefix='/task', tags=["Task"])
app.include_router(point_route, prefix='/point', tags=['Reward'])