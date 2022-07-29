import datetime
from pydantic import BaseModel, Field
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
    username: str | None = None
    email: str | None = None
    password: str
    keyName: KeyNameOfLoginSchema  # Flutter basically send korbe je ami username dici naki email dici.
    # eita user end theke kore ana amar jonno cost saving onek.


class TaskSchema(BaseModel):
    title: str
    icon_id: int
    quote: str
    user_id: int
    frequency_model: str
    frequency: List[str]
    goal: str

    # If goal is set to achieve it all then these values should be null.
    daily_amount_to_reach: int | None = 0
    counting_unit: str | None = None
    when_checking: str | None = "AUTO"
    record_count_when_auto_checking: int | None = 1

    allocated_point: int | None = 0
    point_algorithm: str | None = None
    over_amount_algorithm: str | None = None
    negative_point: int | None = 0
    negative_point_algorithm: str | None = None

    category: int

    reminderTimes: List[str]
    created_at: datetime.datetime | None = datetime.datetime.utcnow()
    updated_at: datetime.datetime | None = datetime.datetime.utcnow()


class TaskCategorySchema(BaseModel):
    category_title: str
