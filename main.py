from fastapi import FastAPI
from database import queries as qs
from database.connection import testebabay

app = FastAPI()

@app.post("/clientes/{id}/transacoes")
def transacoes(id:int, valor:int, tipo:str, descricao:str):
    return {'teste':'teste'}

@app.get('/clientes/{id}/extrato')
def extrato(id:int):
    return {'teste':'teste'}

@app.get("/teste")
def teste():
    select = testebabay()
    return {'test':f'{select}'}
