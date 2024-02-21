from . import connection as cn 
import json

class Query:
    def __init__(self) -> None:
        self.connection = cn.connect()
        self.cursor = self.connection.cursor()

def select():
    query = Query()
    
    select = query.cursor.execute('SELECT * FROM clientes;')
    select = query.cursor.fetchall()
    query.cursor.close()
    return json.dumps(select)




'''
connection = None
# create a cursor
cursor = connection.cursor()
print('PostgreSQL database version: ')
query = cursor.execute('SELECT * FROM pessoa;')
print(query)
query = cursor.fetchall()
print(query)
cursor.close()
return query
'''