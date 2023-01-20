import sqlalchemy as sa
from sqlalchemy import MetaData, Table, Column, Integer, String, Date
from src.database.data_schemes.work_with_db import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Expenses(Base):

    __tablename__ = "expens"
    user_id = Column(Integer)
    operation_id = Column(Integer, primary_key=True)
    cost = Column(Integer)
    disc = Column(String(100))
    date = Column(Date)

class Users(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(25))
    user_hashed_pass = Column(String)
    user_email = Column(String(25))
