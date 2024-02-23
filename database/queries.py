from peewee import *
from datetime import datetime
from fastapi import HTTPException
from .models import BANCO, Cliente, Transacao, Saldo

#bloco de funções de transicão
def fazer_transacao(id:int,valor:int, tipo:str, descricao:str):
    BANCO.connect()
    try:
        clientes = Cliente.select().where(Cliente.id == id)#busca o cliente no banco
        if clientes:#verifica se ele existe
            cliente = clientes[0]
            if len(descricao) <= 10 and tipo == 'c' or tipo =='d':#verifica se os dados da transação são válidos
                if tipo == 'c':
                    dados = creditar(cliente=cliente, valor=valor, descricao=descricao)
                    BANCO.close()
                    return dados
                elif tipo == 'd':
                    dados = debitar(cliente=cliente, valor=valor, descricao=descricao)
                    BANCO.close()
                    return dados
            else:
                BANCO.close()
                raise 422
        else:
            BANCO.close()
            raise 404
        
    except Exception as e:
        BANCO.close()
        return print({f'{e}'})



@BANCO.atomic()
def debitar(cliente:Cliente, valor:int,descricao:str):
    try:
        id =  cliente.id
        limite = cliente.limite
        saldos = Saldo.select().where(Saldo.cliente_id == cliente.id)
        if saldos:
            saldo = saldos[0]
        else:
            saldo = Saldo.create(cliente_id=id, valor=0)

        if valor > limite or saldo.valor - valor < limite*-1:
            return HTTPException(status_code=422, detail="Operação compromete o sistema")
        else:
            transacao = Transacao.create(cliente_id=id, valor=valor, tipo='d', descricao=descricao, realizada_em=str(datetime.now().isoformat()))
            saldo.valor -= valor
            transacao.save()
            saldo.save()
            
            retorno = {
                'limite':cliente.limite,
                'saldo':saldo.valor
            }
            return retorno
    except Exception as e:
        return {f'{e}'}
        

@BANCO.atomic()
def creditar(cliente:Cliente, valor:int, descricao:str):
    try:
        id = cliente.id
        saldos = Saldo.select().where(Saldo.cliente_id == cliente.id)
        if saldos:
            saldo = saldos[0]
        else:
            saldo = Saldo.create(cliente_id = id, valor=0)
        transacao = Transacao.create(cliente_id=id, valor=valor, tipo='c', descricao=descricao, realizada_em=str(datetime.now().isoformat()))

        saldo.valor -= valor
        transacao.save()
        saldo.save()
        
        retorno = {
            'limite':cliente.limite,
            'saldo':saldo.valor
        }
        return retorno
    except Exception as e:
        return {f'{e}'}
        





def get_extrato(id:int):
    try:
        clientes = Cliente.select().where(Cliente.id == id)
        if clientes:
            cliente = clientes[0]
            saldo = get_saldo(cliente.id).valor
            data_extrato = datetime.now().isoformat()
            ultimas_transacoes = get_transacoes(cliente.id)
            
            retorno = {
                'saldo':{
                    'total':saldo,
                    'data_extrato':data_extrato,
                    'limite':cliente.limite
                },
                'ultimas_transacoes': ultimas_transacoes
            }
            return retorno
        else:
            raise 404
    except Exception as e:
        return f'{e}'


def get_transacoes(id:int):
    query = Transacao.select().where(Transacao.cliente_id == id)
    transacoes = []
    transacao = {}

    for i in query:
        transacao = {
            'valor':i.valor,
            'tipo':i.tipo,
            'descricao':i.descricao,
            'realizada_em':i.realizada_em
        }
        transacoes.append(transacao)

    return transacoes

def get_saldo(id:int):
    saldo = Saldo.get(Saldo.cliente_id == id)
    return saldo
    





















def retornar_clientes():
    BANCO.connect()

    clientes = Cliente.select()
    obj = {}
    obj['clientes'] = []
    cliente ={}
    
    for i in clientes:
        cliente = {
            'id':i.id,
            'nome':i.nome,
            'limite':i.limite
        }
        obj['clientes'].append(cliente)
    return obj



def retorna_transacoes(id:int):
    BANCO.connect()