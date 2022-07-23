from datetime import date
from pydantic import BaseModel, Field
from typing import List
from enum import Enum



class Settings(BaseModel):
    authjwt_secret_key : str = "b175098749eeb8bbcd1ffe17ccf650685fe5021a4af5ae29098201e1896cfe890e5a6622121990f32b0354e89fc42783b73a"


class SignupSchema(BaseModel):
    username : str
    email : str 
    first_name : str 
    last_name : str
    password : str 



class KeyNameOfLoginSchema(Enum):
    username = "username"
    email = "email"

class LoginSchema(BaseModel):
    username : str | None = None
    email: str | None = None
    password : str 
    keyName : KeyNameOfLoginSchema #Flutter basically send korbe je ami username dici naki email dici.
        # eita user end theke kore ana amar jonno cost saving onek. 

 

class TaskSchema(BaseModel):
    title : str
    description: str 
    schedule : List[str]