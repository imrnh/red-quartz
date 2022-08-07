from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost/TIME_TRACKER"  # --> Postgres

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://redq:12345678@localhost:3306/TIME_TRACKER"  # MYSQL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
