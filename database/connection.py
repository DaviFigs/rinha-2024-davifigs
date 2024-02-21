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
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)
        return connection
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


from peewee import *

banco = PostgresqlDatabase('banco-teste', user='postgres', password='postgres', host='localhost', port=5432)

class Cliente(Model):
    nome = CharField(max_length=50)
    limite = IntegerField(null=False)
    class Meta:
        database = banco
        table_name = 'clientes'


def testebabay():
    banco.connect()

    clientes = Cliente.select()
    print(type(clientes))
    obj = {}
    lista = []

    for i in clientes:
        lista.append(i)

    print(lista)
    return lista