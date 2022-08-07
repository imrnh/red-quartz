import datetime
from pydantic import BaseModel, Field
from typing import Union
from typing import List
from enum import Enum


class Settings(BaseModel):
    authjwt_secret_key: str = "b175098749eeb8bbcd1ffe17ccf650685fe5021a4af5ae29098201e1896cfe890e5a6622121990f32b0354e89fc42783b73a"


class SignupSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


class KeyNameOfLoginSchema(Enum):
    username = "username"
    email = "email"


class LoginSchema(BaseModel):
    username: Union[str, None] = None
    email: Union [str, None] = None
    password: str
    keyName: KeyNameOfLoginSchema  # Flutter basically send korbe je ami username dici naki email dici.
    # eita user end theke kore ana amar jonno cost saving onek.


class TaskSchema(BaseModel):
    title: str
    icon_id: int
    quote: str
    frequency_model: str
    frequency: List[str]
    goal: str

    # If goal is set to achieve it all then these values should be null.
    daily_amount_to_reach: Union[int, None] = 0
    counting_unit: Union [str, None] = None
    when_checking: Union [str, None] = "AUTO"
    record_count_when_auto_checking: Union [int, None] = 1

    allocated_point: Union [int, None] = 0
    point_algorithm: Union [str, None] = None
    over_amount_algorithm: Union [str, None] = None
    negative_point: Union [int, None] = 0
    negative_point_algorithm: Union [str, None] = None

    category: int

    reminderTimes: List[str]


class TaskCategorySchema(BaseModel):
    category_title: str


class RegisterPointsSchema(BaseModel):
    current_task: int
    units_completed: int
    negative_units: Union[int, None] = 0
    point_registered: Union [datetime.datetime, None] = datetime.datetime.utcnow()
