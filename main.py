from fastapi import FastAPI, HTTPException
from database import queries as qr
app = FastAPI()

@app.post("/clientes/{id}/transacoes")
async def transacoes(id:int, valor:int, tipo:str, descricao:str):
    select = qr.fazer_transacao(id, valor, tipo, descricao)
    if type(select) == dict:
        return select
    else:
        raise HTTPException(status_code=select)

@app.get('/clientes/{id}/extrato')
async def extrato(id:int):
    select = qr.get_extrato(id=id)
    if type(select) == dict:
        return select
    else:
        raise HTTPException(status_code=select)