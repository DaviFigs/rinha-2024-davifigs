from peewee import *
from datetime import datetime
from fastapi import HTTPException
from .models import BANCO, Cliente, Transacao, Saldo


#FUNÇÕES ASSOCIADAS AO PRIMEIRO ENDPOINT (/clientes/id/transacoes)
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
                    if debitar == 422:
                        return 422
                    BANCO.close()
                    return dados
            else:
                BANCO.close()
                return 422
        else:
            BANCO.close()
            return 404
        
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
            return 422
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
        

#FUNÇÕES ASSOCIADAS AO SEGUNDO ENDPOINT /clientes/id/extrato



def get_extrato(id:int):
    try:
        BANCO.connect()
        clientes = Cliente.select().where(Cliente.id == id)
        if clientes:
            cliente = clientes[0]
            saldo = get_saldo(cliente.id)
            #print(f'saldo:{saldo} ')
            data_extrato = datetime.now().isoformat()
            ultimas_transacoes = get_transacoes(cliente.id)
            #print(ultimas_transacoes)
            
            if ultimas_transacoes == 404 or saldo == 404:
                BANCO.close()
                return 404
            
            retorno = {
                'saldo':{
                    'total':saldo.valor,
                    'data_extrato':data_extrato,
                    'limite':cliente.limite
                },
                'ultimas_transacoes': ultimas_transacoes
            }
            BANCO.close()
            return retorno
        else:
            BANCO.close()
            return 404
    except Exception as e:
        BANCO.close()
        return f'{e}'


def get_transacoes(id:int):
    query = Transacao.select().where(Transacao.cliente_id == id).order_by(-Transacao.realizada_em).limit(10)
    if query: 
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
    else:
        return 404

def get_saldo(id:int):
    saldos = Saldo.select().where(Saldo.cliente_id == id)
    if saldos:
        saldo = saldos[0]
        return saldo
    else:
        return 404
    