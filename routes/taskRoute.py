from fastapi import APIRouter

task_router = APIRouter()

@task_router.post("/")
async def create_new_task():
    return {"Hey"}