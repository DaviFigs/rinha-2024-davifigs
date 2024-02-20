from database.connection import return_session
from database import models

def teste1():
    session = return_session()
    clientes = session.query(models.Clientes).all()
    print(clientes)
