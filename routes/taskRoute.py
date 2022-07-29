from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_jwt_auth import AuthJWT
from database.db_config import SessionLocal, engine

from database.models import TaskModel
from database.schemas import TaskSchema

task_router = APIRouter()
session = SessionLocal(bind=engine)


@task_router.post("/create")
async def create_new_task(new_task: TaskSchema, authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    current_user = authorize.get_jwt_subject()
    # user can have multiple task with same name and same execution time.

    new_task_db_instance = TaskModel(
        title=new_task.title,
        icon_id=new_task.icon_id,
        quote=new_task.quote,
        user_id=current_user,
        frequency_model=new_task.frequency_model,
        frequency=new_task.frequency,
        goal=new_task.goal,
        daily_amount_to_reach=new_task.daily_amount_to_reach,
        counting_unit=new_task.counting_unit,
        when_checking=new_task.when_checking,
        record_count_when_auto_checking=new_task.record_count_when_auto_checking,
        allocated_point=new_task.allocated_point,
        point_algorithm=new_task.point_algorithm,
        over_amount_algorithm=new_task.over_amount_algorithm,
        negative_point=new_task.negative_point,
        negative_point_algorithm=new_task.negative_point_algorithm,
        category=new_task.category,
        reminderTimes=new_task.reminderTimes,
        created_at=new_task.created_at,
        updated_at=new_task.updated_at
    )
    session.add(new_task_db_instance)
    session.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "detail": "New task has been created"
    }


@task_router.get('/view')
async def view_tasks(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    current_user = authorize.get_jwt_subject()
    