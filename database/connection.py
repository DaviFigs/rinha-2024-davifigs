from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def return_session():
    Session = sessionmaker(bind=return_engine())
    session = Session()
    return session

def return_engine():
    CONN_STRING = "postgresql://admin:123@db:5433/rinha"
    #CONN_STRING = "postgresql://postgres:postgres@localhost:5432/banco-teste"
    engine = create_engine(CONN_STRING, echo=True)
    return engine