from peewee import *
from datetime import datetime
from .models import BANCO, Cliente, Transacao, Saldo


#validar cliente
#validar transicao
#efetuar transicao de modo que as duas sejam feitas
#verificar se a transição feita não excede o limite de sua conta
#atualizar saldo do cliente (diminuindo o valor da transicao que ele fez)
def fazer_transacao(id:int,valor:int, tipo:str, descricao:str):
    BANCO.connect()
    try:
        clientes = Cliente.select().where(Cliente.id == id)#busca o cliente no banco
        if clientes:#verifica se ele existe
            if len(descricao) <= 10 and tipo == 'c' or tipo =='d':#verifica se os dados da transação são válidos

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