from fastapi import APIRouter, HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash  # To hash password.
from database.db_config import SessionLocal, engine
from database.schemas import SignupSchema
from database.models import UserModel
from utilities.Signup_data_modification import remove_whitespaces_from_front_and_rear, username_validator

authRouter = APIRouter()
session = SessionLocal(bind=engine)


# ------------------------------------
# ------------------------------------
#               
#               SIGNUP 
#
# ------------------------------------
# ------------------------------------

@authRouter.post("/register")
async def register(newUser: SignupSchema):
    newUser = remove_whitespaces_from_front_and_rear(newUser) 
    raised_exception: HTTPException = username_validator(newUser.username) #If no exception is raised, this will return null.
    
    if raised_exception:
        return raised_exception

    # Checking uniqueness of the email and username
    db_username = session.query(UserModel).filter(UserModel.username==newUser.username).first()
    db_email = session.query(UserModel).filter(UserModel.email==newUser.email).first()

    if db_username is not None:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail = "User with same username already exists" )
    
    if db_email is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User with same email already exists")
    



    return {
        "name": newUser.first_name + " " + newUser.last_name,
        "username": newUser.username,
        "email": newUser.email,
        "password": newUser.password,
    }







# ------------------------------------
# ------------------------------------
#               
#               LOGIN 
#
# ------------------------------------
# ------------------------------------

@authRouter.post("/login")
async def login():
    return {"Logged in"}