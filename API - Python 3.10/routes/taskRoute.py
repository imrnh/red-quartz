import datetime

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_jwt_auth import AuthJWT
from database.db_config import SessionLocal, engine
from fastapi.encoders import jsonable_encoder

from database.models import TaskModel
from database.schemas import TaskSchema

task_router = APIRouter()
session = SessionLocal(bind=engine)


@task_router.post("/create")
async def create_new_task(new_task: TaskSchema, authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        # user can have multiple task with same name and same execution time.

        try:
            new_task_db_instance = TaskModel(
                title=new_task.title,
                icon_id=new_task.icon_id,
                quote=new_task.quote,
                user_id=current_user,
                frequency_model=new_task.frequency_model,
                frequency=new_task.frequency,
                goal=new_task.goal,
                daily_amount_to_reach=new_task.daily_amount_to_reach,
                counting_unit=new_task.counting_unit.capitalize(),  # in the following formate: Time, Units, Seconds
                when_checking=new_task.when_checking,
                record_count_when_auto_checking=new_task.record_count_when_auto_checking,
                allocated_point=new_task.allocated_point,
                point_algorithm=new_task.point_algorithm,
                over_amount_algorithm=new_task.over_amount_algorithm,
                negative_point=new_task.negative_point,
                negative_point_algorithm=new_task.negative_point_algorithm,
                category=new_task.category,
                reminderTimes=new_task.reminderTimes,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow()
            )
            session.add(new_task_db_instance)

        except Exception as child_exception:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Something went wrong")

    except Exception as parent_exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    session.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "detail": "New task has been created"
    }


@task_router.get('/get_all')
async def view_tasks(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        if current_user is not None:
            db_task = session.query(TaskModel).filter(TaskModel.user_id == current_user).all()
            all_task_list = list(db_task)

            return jsonable_encoder(all_task_list)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@task_router.get('/update_dates_of_task')
async def get_last_updated_dates_of_all_the_task(authorize: AuthJWT = Depends()): # This function will return task id and task update dates
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()

        update_dates_and_ids = session.query(TaskModel.id, TaskModel.updated_at).filter(TaskModel.user_id == current_user).all()

        return jsonable_encoder(list(update_dates_and_ids))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)