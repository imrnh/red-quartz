from db_config import engine, Base
#from models import User, Order -- import kore tarpor run korte hobe.
from models import UserModel

Base.metadata.create_all(bind = engine) #Creating the table.