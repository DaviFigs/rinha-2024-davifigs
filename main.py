from fastapi import FastAPI
from database import queries as qr
import json
app = FastAPI()

@app.post("/clientes/{id}/transacoes")
def transacoes(id:int, valor:int, tipo:str, descricao:str):
    dados = qr.retorna_transacoes(id)
    return {'teste':'teste'}

@app.get('/clientes/{id}/extrato')
def extrato(id:int):
    return {'teste':'teste'}

@app.get("/teste")
def teste():
    select = qr.retornar_clientes()
    return select
