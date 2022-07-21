from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
from sqlalchemy_utils.types import ChoiceType 
import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType


class User(Base):

    USER_PAYMENT_TYPE = (
        ("TRIAL","Free-Trial"), # That means user is on free trial
        ("SUB","Paid"), # This means user is paid. When it is set to sub, we will have another table to track subscription starting date to end date and offer full service.
        ("FREE","Free") # This means user is a free user. This may not be available. Still just created here for the purpose of code reusing if we need it later.
    )

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique = True)
    email = Column(String(130), unique = True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    password = Column(Text, nullable = True)
    payment_status = Column(ChoiceType(USER_PAYMENT_TYPE), default = "TRIAL") 
    subscription_Started = Column(DateTime, nullable = False) #The day of the creation of acc will be here. 
        # Now, as creating an account leads to 30 days free trial, this without paying will be the time when free trial started. 
        # And by based on payment status, we will understand if he is a free-trial user or paid user. 
        # But for offering our services, the date stored here should not be older than 30 days.
    created_at = Column(DateTime, default = datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable = True)
    orders = relationship('TaskCategories', back_populates='user')


    def __repr__ (self):
        return f"<User {self.username} >"



class TaskCategories(Base): # Category for task. Like section in Tick Tick.
        __tablename__ = "user_defined_task_categories"
        id = Column(Integer, primary_key=True)
        category_title = Column(String(25), nullable = False)
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship('User', back_populates='user_defined_task_categories')
    




class Task(Base):

        GOAL_TYPE = (
                ("ACHIEVE_ALL", "Achieve-it-all"), # Mane task ta protidin ekbar e hobe. Jemon care for face jeta ache amar tick tick e.
                ("CERTAIN_AMOUNT", "Reach a certain amount") # Etay limit set kore dibe je dine koto bar korbe ba koto hr korbe.
                        # Eta set korei ashole algorithm set korte parbe. Nahoy algorithm set korte parbena.
        )

        WHEN_CHECKING = (
                ("AUTO","Auto"),
                ("MANUAL", "Manual")
        )

        __tablename__ = "tasks"
        id = Column(Integer, primary_key = True)
        title = Column(String(100), nullable = False)
        iconId = Column(Integer()) # This data will be sent to front-end as integer. And front-end will handle it itself. 
                # These icons will be saved as png in the front-end. 
        short_description = Column(Text)

        goal = Column(ChoiceType(GOAL_TYPE), default = "ACHIEVE_ALL")
                # Nicher daily_amount_to_reach theke record_count porjonto bujhte tick tick er task create korte giye goal reach e certain amount diye check korlei hobe. Okhaner motoi.
        daily_amount_to_reach = Column(Integer, default = 1)
        countng_unit = Column(String(25), default = "Count") # Ei unit ta sob task create er time e alada vabe create korte hobe. 
                # Create kora validation o mangement Eta flutter er kaj. Flutter api ke ekta srting akare pathabe. API string tai rakhbe database e.
        when_checking = Column(ChoiceType(WHEN_CHECKING), default= "AUTO")
        record_count_when_auto_checking = Column(Integer, default = 0) # When user will set auto checking, he/she will set this to a particular no.
                # This no will represent, for one checking, how much time it will be done.
                # -- But manual count hole protibar user pathabe je koto count add korte.\


        
        allocated_point = Column(Integer, default = 0)
        point_algorithm = Column(Text, nullable = True)
        negative_point = Column(Integer, default = 0)
        negative_point_algorithm = Column(Text, nullable=True)



        section = Column(Integer, ForeignKey('user_defined_task_categories.id')) #This is actually category of task. User will create the category himself.
                # Task creation route will retrive all the category names from TaskCategories table and will send it to flutter.
                # Later while creating task, Flutter will save the id which is the id of a certain cateogory in the TaskCategories table.

        reminderTimes = Column(MutableList.as_mutable(PickleType()), default = [])
                # This will work only on the days where the task will be needed to executed.
                # These days will be selected by the user either by date or weekly repeat cycle or interval cycle.




























"""
    --> schedule is a list of string. These strings are actually date time and day_of week.
            The formate is: "YYYY-MM-DD HOUR:MIN DAY_OF_WEEK" 
            An example is: "2022-08-03 10:30 4" -> 3 August 2022, 10:30 AM and 4th day of the week.
            Counting of the week starts from Saturday. So, 4 means Tuesday.

                    Sat - 1  |  Mon - 3  |  Wed - 5  | Fri - 7
                    Sun - 2  |  Tue - 4  |  Thu - 6  |

    --> in_repeatCard stores boolean data. Either false or true.
            If it is set to True, that means this task is in the repeat card and don't need to execute it in the time given in the schedule.
            But, we haven't cleared the schedule in case the user remove it from the repeat card, it will be a big hassle to add the repeating time again.
            Instead, while the task is being added to repeat card, the in_repeatCard will be set to true and out_repeatCard will be set to False.
            This way we will not execute it outside repeat card without further information.
"""

class OldTaskTable(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True)
    title : Column(String(100), nullable = False)
    description : Column(Text)

    #schedule will contain list of strings. Every item on the list will contain the date, the time and the day of the week. 
    schedule = Column(MutableList.as_mutable(PickleType), default=[]) 
    in_repeatCard: Column(Boolean, default = False) #If this is true, that means, this task is in the repeat card.
    out_repeatCard: Column(Boolean, default = True) #If this is true, that means, this task will be in todo list of the user for the time in schedule.

    alloc_point_total : Column(Integer, nullable = False)
    alloc_algorithm: Column(String(), nullable = False)
    negative_point : Column(Integer, nullable = True)
    neg_point_alorithm: Column(String(), nullable = True)

            #--- N.D... TaskExecutionTime class is not ready yet.
