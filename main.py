from fastapi import FastAPI
from database.connection import connect

app = FastAPI()

@app.post("/clientes/{id}/transacoes")
def transacoes(id:int, valor:int, tipo:str, descricao:str):
    return {'teste':'teste'}

@app.get('/clientes/{id}/extrato')
def extrato(id:int):
    return {'teste':'teste'}

@app.get("/teste")
def teste():
    query = connect()
    return {'test':f'{query}'}
