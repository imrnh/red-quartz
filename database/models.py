from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
from sqlalchemy_utils.types import ChoiceType 
import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType


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
    repeatOn = Column(MutableList.as_mutable(PickleType), default=[]) #this will contain list of strings. 
        # Every item on the list will contain the date, the time and the day of the week. 
    alloc_point_total : Column(Integer, nullable = False)
    alloc_algorithm: Column(String(), nullable = False)
    negative_point : Column(Integer, nullable = False)

            #--- N.D... TaskExecutionTime class is not ready yet.