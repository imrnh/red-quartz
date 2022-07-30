from types import NoneType
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

from database.db_config import SessionLocal, engine
from database.schemas import SignupSchema, LoginSchema
from database.models import UserModel

from utilities.Signup_data_modification_and_validation import remove_whitespaces_from_front_and_rear, username_validator, check_password_ok
from utilities.check_valid_email import is_valid_email

authRouter = APIRouter()
session = SessionLocal(bind=engine)


# ______________ REGISTER ______________

@authRouter.post("/register", status_code=status.HTTP_201_CREATED)
async def register(new_user: SignupSchema):
    new_user = remove_whitespaces_from_front_and_rear(new_user)

    raised_exception: HTTPException = username_validator(
        new_user.username)  # If no exception is raised, this will return null.
    if raised_exception:raise raised_exception

    invalid_email: HTTPException = is_valid_email(new_user.email)
    if invalid_email: raise invalid_email

    invalid_password: HTTPException = check_password_ok(new_user.password)  # If no exception is raised, this will return null.
    if invalid_password: raise invalid_password

    # Checking uniqueness of the email and username
    db_username = session.query(UserModel).filter(UserModel.username == new_user.username).first()
    db_email = session.query(UserModel).filter(UserModel.email == new_user.email).first()

    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with same username already exists")
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with same email already exists")

    new_user_db_object = UserModel(
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        password=new_user.password
    )

    session.add(new_user_db_object)
    session.commit()

    return HTTPException(status_code=status.HTTP_201_CREATED, detail='User created')


# _________________ LOGIN __________________

@authRouter.post("/login", status_code=status.HTTP_200_OK)
async def login(login_request: LoginSchema, authorize: AuthJWT = Depends()):

    def token_generate_for_this_user(logged_userid):
        access_token = authorize.create_access_token(subject=logged_userid, user_claims={'username': logged_userid})
        refresh_token_ = authorize.create_refresh_token(subject=logged_userid)
        response = {
            'access': access_token,
            'refresh': refresh_token_
        }
        return jsonable_encoder(response)

    # ___________________ LOGIN with username ____________________
    if login_request.keyName.name == "username":  # ___ LOGIN USING USERNAME
        if type(login_request.username) is not NoneType:
            raised_exception_username_validation = username_validator(login_request.username)

            if raised_exception_username_validation:
                return raised_exception_username_validation

            db_user = session.query(UserModel).filter(UserModel.username == login_request.username).first()
            if type(db_user) is not NoneType:
                if db_user.password == login_request.password:  # if both password matches.
                    return token_generate_for_this_user(db_user.id)
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password.")
            else:  # if type(db_user) is not NoneType
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No account found")
        else:  # if type(req.username) is not NoneType
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Key is username & username empty")

    # --------------------- LOGIN with email ---------------------
    elif login_request.keyName.name == "email":
        if type(login_request.email) is not NoneType:
            valid_email = is_valid_email(login_request.email)  # Checking the validity of the email address
            if not valid_email:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a valid email")
            db_user = session.query(UserModel).filter(UserModel.email == login_request.email).first()
            if type(db_user) is not NoneType:
                if db_user.password == login_request.password:  # if both password matches.
                    return token_generate_for_this_user(db_user.username)
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password.")
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No account found with this email")
        else:  # if type(req.username) is not NoneType
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Key is email but email empty")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=" Keyname can be only 'username' or 'email'")


# ______________ REFRESH TOKEN GENERATOR ______________

@authRouter.get("/refresh")
async def refresh_token(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Require valid refresh token")

    access_token = authorize.create_access_token(subject=authorize.get_jwt_subject())
    refresh_token_ = authorize.create_refresh_token(subject=authorize.get_jwt_subject())

    return jsonable_encoder(
        {
            "access-token": access_token,
            "refresh-token": refresh_token_
        }
    )


# Tutorial function of how to lock a function and how to show username after user is logged in.
@authRouter.get("/userid")
def get_username(authorize: AuthJWT = Depends()):

    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    current_user = authorize.get_jwt_subject()

    return {"user_id": current_user}