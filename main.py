from fastapi import FastAPI, HTTPException
from database import queries as qr
import json
app = FastAPI()

@app.post("/clientes/{id}/transacoes")
def transacoes(id:int, valor:int, tipo:str, descricao:str):
    select = qr.fazer_transacao(id, valor, tipo, descricao)
    return select

@app.get('/clientes/{id}/extrato')
def extrato(id:int):
    return {'teste':'teste'}
