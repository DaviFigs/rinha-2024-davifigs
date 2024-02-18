from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONN_STRING = create_engine("postgresql+psycopg2://admin:123@localhost:5433/rinha")
engine = create_engine(CONN_STRING, echo=True)

def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



