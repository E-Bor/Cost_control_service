from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# create database engine
engine = create_engine("sqlite:///./database.sqlite3")

# create session
session = Session(bind=engine)


# session generator
def get_session() -> Session:
    try:
        yield session
    finally:
        session.close()
