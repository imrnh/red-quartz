from database import engine, Base
#from models import User, Order -- import kore tarpor run korte hobe.


Base.metadata.create_all(bind = engine) #Creating the table.