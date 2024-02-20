from fastapi import FastAPI
from testes import teste1

app = FastAPI()

@app.post("/clientes/{id}/transacoes")
def transacoes(id:int, valor:int, tipo:str, descricao:str):
    return {'teste':'teste'}

@app.get('/clientes/{id}/extrato')
def extrato(id:int):
    return {'teste':'teste'}

@app.get("/teste")
def teste():
    teste1.teste1()
