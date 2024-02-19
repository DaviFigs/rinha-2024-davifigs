from database.connection import return_engine

conn = return_engine().connect()
trans = conn.begin()

comando = """
    select * from clientes;

"""
clientes = conn.execute(comando)
trans.commit()
conn.close()

print(clientes)