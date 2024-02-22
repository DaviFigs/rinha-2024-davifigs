from peewee import *
from datetime import datetime
from .models import BANCO, Cliente, Transacao, Saldo


#validar cliente
#validar transicao
#efetuar transicao de modo que as duas sejam feitas
#verificar se a transição feita não excede o limite de sua conta
#atualizar saldo do cliente (diminuindo o valor da transicao que ele fez)

@BANCO.atomic()
def debitar(cliente:Cliente, valor:int):
    try:
        saldo = Saldo.select().where(Saldo.cliente_id == cliente.id)
        limite = cliente.limite
        if valor > limite or saldo.valor - valor < limite*-1:
            return {"erro":'422'}
        else:
            pass
    except Exception as e:
        return {f'{e}'}
        


    
def creditar(id:int, valor:int):
    pass



def fazer_transacao(id:int,valor:int, tipo:str, descricao:str):
    BANCO.connect()
    try:
        clientes = Cliente.select().where(Cliente.id == id)#busca o cliente no banco
        if clientes:#verifica se ele existe
            cliente = clientes[0]
            print(cliente.nome)
            if len(descricao) <= 10 and tipo == 'c' or tipo =='d':#verifica se os dados da transação são válidos

                if tipo == 'c':
                    creditar()
                elif tipo == 'd':
                    debitar()







                #verificar o tipo de transação e se ela satisfaz as condições da rinha

                #efetua transição de fato (precisamos atualizar os dados do cliente!)
                transacao = Transacao.create(cliente_id = id, valor=valor, tipo=tipo, descricao =descricao, realizada_em=str(datetime.now().isoformat()))
                print('transacao criada')
                print(transacao.valor, transacao.realizada_em)
            else:
                print('descricao maior que 10 caracteres ou operação inválida!')
        else:
            print('cliente nao existe!')
        
    except Exception as e:
        return print({f'{e}'})
























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