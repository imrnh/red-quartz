import datetime
from dateutil import relativedelta
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

from database.db_config import SessionLocal, engine
from database.models import PointsModel, TaskModel
from database.schemas import RegisterPointsSchema
from utilities.reward_expression_decoder import decode_reward_expression, extra_units_reward_eval, negative_points

point_route = APIRouter()
session = SessionLocal(bind=engine)


@point_route.post("/new_reward")
def register_point(new_points: RegisterPointsSchema,
                   authorize: AuthJWT = Depends()):  # Achieve it all hole units_complete e 1 thakbe.
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    this_task = session.query(TaskModel).filter(TaskModel.id == new_points.current_task,
                                                TaskModel.user_id == current_user).first()
    credited = 0

    if this_task:
        if this_task.goal == "ACHIEVE_ALL":
            if new_points.units_completed > 0:
                credited = this_task.allocated_point
                print("____ UNIT > 0")
            else:
                credited = - this_task.negative_point
                print("___ UNIT < 0")

        elif this_task.goal == "CERTAIN_AMOUNT":

            def calculate_points():
                calculated_value = decode_reward_expression(TaskModel.point_algorithm, new_points.units_completed,
                                                            TaskModel.daily_amount_to_reach,
                                                            TaskModel.allocated_point)

                return calculated_value

            if new_points.units_completed < this_task.daily_amount_to_reach:
                credited = calculate_points()

            elif new_points.units_completed == this_task.daily_amount_to_reach:
                credited = TaskModel.allocated_point

            elif new_points.units_completed > this_task.daily_amount_to_reach:
                extra_units = new_points.units_completed - this_task.daily_amount_to_reach
                extra_points = extra_units_reward_eval(this_task.over_amount_algorithm, extra_units)

                credited = calculate_points() + extra_points

            elif new_points.units_completed == 0:
                if new_points.negative_units != 0:
                    credited = negative_points(this_task.negative_point_algorithm, new_points.negative_units)
                else:
                    credited = this_task.negative_point

        new_reward_db_instance = PointsModel(
            task_id=new_points.current_task,
            user_id=current_user,
            achieved_point=credited
        )

        session.add(new_reward_db_instance)
        session.commit()

        return {
            "detail": "Reward received"
        }

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@point_route.get(
    '/daily_total/{freq}')  # freq te pass korbo je koto diner total point chai, weekly -> weekly total, daily -> daily total, monthly -> monthly total, yearly -->yearly total
def show_daily_total_points(freq: str, authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()

    except Exception as raised_Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    points_from_db = session.query(PointsModel).filter(PointsModel.user_id == current_user).all()

    if freq == "daily":
        captured_data = [captured_record for captured_record in points_from_db if
                         captured_record.point_registered.date() == datetime.datetime.utcnow().date()]
        points = sum(datax.achieved_point for datax in captured_data)

    elif freq == "weekly":
        current_week = datetime.datetime.utcnow().isocalendar().week
        captured_data = [captured_record for captured_record in points_from_db if
                         captured_record.point_registered.isocalendar().week == current_week]
        points = sum(datax.achieved_point for datax in captured_data)

    elif freq == "monthly":
        captured_data = [captured_record for captured_record in points_from_db if relativedelta.relativedelta(captured_record.point_registered, datetime.datetime.utcnow()).months == 0]
        points = sum(datax.achieved_point for datax in captured_data)

    elif freq == "yearly":
        captured_data = [captured_record for captured_record in points_from_db if relativedelta.relativedelta(captured_record.point_registered, datetime.datetime.utcnow()).years == 0]
        points = sum(datax.achieved_point for datax in captured_data)

    return {
        "Points": points
    }
