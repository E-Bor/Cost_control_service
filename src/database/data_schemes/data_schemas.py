from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

# class constructor initialization
Base = declarative_base()


# expenses table schema
class Expenses(Base):

    __tablename__ = "expens"
    user_id = Column(Integer)
    operation_id = Column(Integer, primary_key=True)
    cost = Column(Integer)
    disc = Column(String(100))
    date = Column(Date)
    category = Column(String(20))


# user table schema
class Users(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(25))
    user_hashed_pass = Column(String)
    user_email = Column(String(25))


# earnings table schema
class Earnings(Base):

    __tablename__ = "earnings"
    user_id = Column(Integer)
    earning_id = Column(Integer, primary_key=True)
    earning_value = Column(Integer)
    date = Column(Date)
