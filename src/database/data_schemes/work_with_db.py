from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("sqlite:///./database.sqlite3")

session = Session(bind=engine)

# Session = sessionmaker(engine)
#
# session = Session()

def get_session() -> Session:
    try:
        yield session
    finally:
        session.close()

