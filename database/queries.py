from peewee import *
import asyncio
from datetime import datetime
from .models import BANCO, Cliente, Transacao, Saldo


#FUNÇÕES ASSOCIADAS AO PRIMEIRO ENDPOINT (/clientes/id/transacoes)
async def fazer_transacao(id:int,valor:int, tipo:str, descricao:str):
    BANCO.connect()
    try:
        clientes = Cliente.select().where(Cliente.id == id)#busca o cliente no banco
        if clientes:#verifica se ele existe
            cliente = clientes[0]
            if len(descricao) <= 10 and tipo == 'c' or tipo =='d':#verifica se os dados da transação são válidos
                if tipo == 'c':
                    dados = await creditar(cliente=cliente, valor=valor, descricao=descricao)
                    BANCO.close()
                    return dados
                elif tipo == 'd':
                    dados = await debitar(cliente=cliente, valor=valor, descricao=descricao)
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
        return print({f'{e} bosta'})



@BANCO.atomic()
async def debitar(cliente:Cliente, valor:int,descricao:str):
    try:
        id = cliente.id
        limite = cliente.limite
        saldos = await Saldo.select().where(Saldo.cliente_id == cliente.id)
        if saldos:
            saldo = saldos[0]
        else:
            saldo = await Saldo.create(cliente_id=id, valor=0)

        if valor > limite or saldo.valor - valor < limite*-1:
            return 422
        else:
            transacao = await Transacao.create(cliente_id=id, valor=valor, tipo='d', descricao=descricao, realizada_em=str(datetime.now().isoformat()))
            saldo.valor -= valor
            await transacao.save()
            await saldo.save()
            
            retorno = {
                'limite':cliente.limite,
                'saldo':saldo.valor
            }
            return retorno
    except Exception as e:
        return {f'{e}'}
        

@BANCO.atomic()
async def creditar(cliente:Cliente, valor:int, descricao:str):
    try:
        id = cliente.id
        saldos =  Saldo.select().where(Saldo.cliente_id == cliente.id)
        if saldos:
            saldo = saldos[0]
        else:
            saldo = await Saldo.create(cliente_id = id, valor=0)
        transacao = await Transacao.create(cliente_id=id, valor=valor, tipo='c', descricao=descricao, realizada_em=str(datetime.now().isoformat()))

        saldo.valor -= valor
        await transacao.save()
        await saldo.save()
        
        retorno = {
            'limite':cliente.limite,
            'saldo':saldo.valor
        }
        return retorno
    except Exception as e:
        return {f'{e}'}
        

#FUNÇÕES ASSOCIADAS AO SEGUNDO ENDPOINT /clientes/id/extrato



async def get_extrato(id:int):
    try:
        BANCO.connect()
        clientes = await Cliente.select().where(Cliente.id == id)
        if clientes:
            cliente = clientes[0]
            saldo = await get_saldo(cliente.id)
            
            data_extrato = await datetime.now().isoformat()
            ultimas_transacoes = await get_transacoes(cliente.id)
            
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


async def get_transacoes(id:int):
    query = await Transacao.select().where(Transacao.cliente_id == id).order_by(-Transacao.realizada_em).limit(10)
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

async def get_saldo(id:int):
    saldos = await Saldo.select().where(Saldo.cliente_id == id)
    if saldos:
        saldo = saldos[0]
        return saldo
    else:
        return 404
    