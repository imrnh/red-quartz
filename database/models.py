from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
from sqlalchemy_utils.types import ChoiceType 
import datetime


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique = True)
    email = Column(String(130), unique = True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    password = Column(Text, nullable = True)
    created_at = Column(DateTime, default = datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable = True)
    updated_total = Column(Integer)


    def __repr__ (self):
        return f"<User {self.username} >"


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True)
    title : Column(String(100), nullable = False)
    description : Column(Text)
    alloc_time : Column(Integer, nullable = False)
    alloc_point_total : Column(Integer, nullable = False)
    negative_point : Column(Integer, nullable = False)
    time_start : Column()   # Time when the task will start
    time_end : Column()     # Time when the task will end.