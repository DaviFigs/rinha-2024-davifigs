'''from sqlalchemy import create_engine
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
'''
import psycopg2
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db

def connect():
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        print('PostgreSQL database version: ')
        crsr.execute('SELECT * FROM clientes;')
        query = crsr.fetchone()
        print(query)
        crsr.close()
        return query
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')

if __name__ == "__main__":
    connect()
