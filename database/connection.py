from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    Session = sessionmaker(bind=return_engine())
    session = Session()
    return session

def return_engine():
    CONN_STRING = "postgresql://admin:123@localhost:5433/rinha"
    engine = create_engine(CONN_STRING, echo=True)
    return engine