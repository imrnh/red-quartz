from database.db_config import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType


class UserModel(Base):
    USER_ACCOUNT_STATUS = (
        ("TRIAL", "Free-Trial"),  # That means user is on free trial
        ("SUB", "Paid"),
        # This means user is paid. When it is set to sub, we have subscription_started field to track when subscription was started.
        ("FREE", "Free")
        # This means user is a free user. This may not be available. Still just created here for the purpose of code reusing if we need it later.
    )

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True)
    email = Column(String(130), unique=True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    password = Column(Text, nullable=True)

    account_status = Column(ChoiceType(USER_ACCOUNT_STATUS), default="TRIAL")
    subscription_Started = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    # The day of the creation of acc will be here.
    # Now, as creating an account leads to 30 days free trial, this without paying will be the time when free trial started.
    # And by based on payment status, we will understand if he is a free-trial user or paid user.
    # But for offering our paid services, the date stored here should not be older than 30 days.
    # if the user get demoted to free user, we will clear the date.

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User {self.username} >"


class TaskModel(Base):

    FREQUENCY = (
        ("Daily", "daily"),
        ("Weekly", "weekly"),
        ("Interval", "interval"),
        ("Custom", "custom")
    )

    GOAL_TYPE = (
        ("ACHIEVE_ALL", "achieve_all"),
        ("CERTAIN_AMOUNT", "certain_amount")
    )

    WHEN_CHECKING = (
        ("AUTO", "Auto"),
        ("MANUAL", "Manual")
    )

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    icon_id = Column(Integer())
    quote = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('UserModel')

    frequency_model = Column(ChoiceType(FREQUENCY), default="daily")
    frequency = Column(MutableList.as_mutable(PickleType()), default=[])

    # Nicher daily_amount_to_reach theke record_count porjonto bujhte tick tick er task create korte giye goal reach e certain amount diye check korlei hobe. Okhaner motoi.
    goal = Column(ChoiceType(GOAL_TYPE), default="ACHIEVE_ALL")
    daily_amount_to_reach = Column(Integer, default=1)
    counting_unit = Column(String(25),default="Count")  # Ei unit ta sob task create er time e alada vabe create korte hobe.
    # Create kora validation o mangement Eta flutter er kaj. Flutter api ke ekta srting akare pathabe. API string tai rakhbe database e.
    when_checking = Column(ChoiceType(WHEN_CHECKING), default="AUTO")
    record_count_when_auto_checking = Column(Integer, default=0)  # When user will set auto checking, he/she will set this to a particular no.
    # This number represents: for one checking, how much unit to count of daily_amount_to_reach.
    # -- But manual count hole protibar user pathabe je koto count add korte.

    allocated_point = Column(Integer, default=0)
    point_algorithm = Column(Text, nullable=True)
    over_amount_algorithm = Column(Text, nullable=True) # If the user do more units of work than allocated unit.
    negative_point = Column(Integer, default=0)
    negative_point_algorithm = Column(Text, nullable=True)

    category = Column(Integer, ForeignKey('task_category.id'))
    # This is actually category of task. User will create the category himself.
    # Task creation route will retrive all the category names from TaskCategories table and will send it to flutter.
    # Later while creating task, Flutter will save the id which is the id of a certain cateogory in the TaskCategories table.
    # -- Eta integer thakbe. String save korle, pore jokhn user caretogory name change korbe tkhn abar change kora lagbe.

    reminderTimes = Column(MutableList.as_mutable(PickleType()), default=[])
    # The type of this will be string.
    # This will work only on the days when the task will be needed to execute.
    # These days will be selected by the user either by date or weekly repeat cycle or interval cycle.

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class TaskCategoryModel(Base):  # Category for task. Like section in Tick Tick.
    __tablename__ = "task_category"
    id = Column(Integer, primary_key=True)
    category_title = Column(String(25), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('UserModel')


class PointsModel(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key = True)
    task_id = Column(Integer, ForeignKey('task.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    achieved_point = Column(Integer, default = 0)
    point_registered = Column(DateTime, default = datetime.datetime.utcnow())
    user = relationship('UserModel')
    task = relationship('TaskModel')


class TaskCompletionDetailsModel(Base):
    __tablename__ = "task_completion_details"
    id = Column(Integer, primary_key = True)
    task_id = Column(Integer, ForeignKey('task.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    task_completion_ = Column(MutableList.as_mutable(PickleType()), default = [])
    user = relationship('UserModel')
    task = relationship('TaskModel')