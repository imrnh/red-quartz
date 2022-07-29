from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from database.db_config import SessionLocal, engine

from database.models import TaskCategoryModel
from database.schemas import TaskCategorySchema

task_category_router = APIRouter()
session = SessionLocal(bind=engine)


@task_category_router.post("/create_new")
async def get_category_names(new_category: TaskCategorySchema, authorize: AuthJWT = Depends()):

    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    current_user = authorize.get_jwt_subject()

    db_task_category = session.query(TaskCategoryModel).filter(TaskCategoryModel.user_id == current_user).all() # Retrieving all the category names for that user.

    list_of_all_categories_available_for_this_user = []
    if db_task_category:
        for single_category in db_task_category:
            list_of_all_categories_available_for_this_user.append(single_category.category_title)

    if new_category.category_title.capitalize() in list_of_all_categories_available_for_this_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= "Category name already exists")

    ls = []

    new_category_db_object = TaskCategoryModel( category_title = new_category.category_title.capitalize(), user_id = current_user)
    session.add(new_category_db_object)
    session.commit()

    return jsonable_encoder({
        "status_code": status.HTTP_201_CREATED,
        "detail": "New category has been created"
    })


@task_category_router.get("/view")
async def view_category(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    current_user = authorize.get_jwt_subject()

    db_task_categories = session.query(TaskCategoryModel).filter(TaskCategoryModel.user_id == current_user).all()

    return {"categories": list(db_task_categories)}
