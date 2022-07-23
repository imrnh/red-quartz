from types import NoneType
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash  # To hash password.
from database.db_config import SessionLocal, engine
from database.schemas import SignupSchema, LoginSchema
from database.models import UserModel
from utilities.Signup_data_modification import remove_whitespaces_from_front_and_rear, username_validator
from utilities.check_valid_email import is_valid_email

authRouter = APIRouter()
session = SessionLocal(bind=engine)



# ------------------------------------
#               
#               SIGNUP 
#
# ------------------------------------

@authRouter.post("/register", status_code=status.HTTP_201_CREATED)
async def register(newUser: SignupSchema):
    newUser = remove_whitespaces_from_front_and_rear(newUser) 
    raised_exception: HTTPException = username_validator(newUser.username) #If no exception is raised, this will return null.
    
    if raised_exception:
        return raised_exception
    
    valid_email = is_valid_email(newUser.email)
    if not valid_email:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Given email address is not a valid email address.")

    # Checking uniqueness of the email and username
    db_username = session.query(UserModel).filter(UserModel.username==newUser.username).first()
    db_email = session.query(UserModel).filter(UserModel.email==newUser.email).first()

    if db_username is not None:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail = "User with same username already exists" )
    
    if db_email is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User with same email already exists")
    
    

    new_user_db_object = UserModel(
        username = newUser.username,
        email = newUser.email,
        first_name = newUser.first_name,
        last_name = newUser.last_name,
        #password = generate_password_hash(newUser.password)
        password = newUser.password
    )

    session.add(new_user_db_object)
    session.commit()

    # return {
    #     "name": newUser.first_name + " " + newUser.last_name,
    #     "username": newUser.username,
    #     "email": newUser.email,
    #     "password": newUser.password,
    # }

    return HTTPException(status_code=status.HTTP_201_CREATED, detail= 'User created')






# ------------------------------------
#               
#               LOGIN 
#
# ------------------------------------

@authRouter.post("/login", status_code= status.HTTP_200_OK)
async def login(req: LoginSchema, Authorize: AuthJWT = Depends()):

    def token_generate_for_this_user(usrnme):
        access_token = Authorize.create_access_token(subject=usrnme, user_claims={'username': usrnme})
        refresh_token = Authorize.create_refresh_token(subject=usrnme)
        response = {
            'access' : access_token,
            'refresh': refresh_token
        }
        return jsonable_encoder(response)


    if req.keyName.name == "username":
        if type(req.username) is not NoneType:
            db_user = session.query(UserModel).filter(UserModel.username==req.username).first()
            if type(db_user) is not NoneType:
                #data fetched. Now handle login logic
                if db_user.password == req.password: #if both password matches.
                    return token_generate_for_this_user(db_user.username)
                else:
                     raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password.")


            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No account found with this username")   
        else: #if type(req.username) is not NoneType
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail = "Username is empty but asked to login with username")
    



    elif req.keyName.name == "email":
        if type(req.email) is not NoneType:
            valid_email = is_valid_email(req.email) #Checking the validity of the email address
            if not valid_email:
                raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Given email address is not a valid email address.")

            db_user = session.query(UserModel).filter(UserModel.email==req.email).first()
            
            if type(db_user) is not NoneType:
                # data fetched now. Now handle login logic.
                if db_user.password == req.password: #if both password matches.
                    return token_generate_for_this_user(db_user.username)
                else:
                     raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password.")



            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No account found with this email")   
        else: #if type(req.username) is not NoneType
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail = "Email is empty but asked to login with email")




    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Seems like a middle man attack. Keyname can be only 'username' or 'email'. Anything else is forbidden.")





# -------------------------------------------------
#               
#            REFRESH TOKEN GENERATOR 
#
# -------------------------------------------------




@authRouter.get("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Require valid refresh token")

    access_token = Authorize.create_access_token(subject=Authorize.get_jwt_subject())
    
    return jsonable_encoder(
        {"accesstoken": access_token}
    )  