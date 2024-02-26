from peewee import *

BANCO = PostgresqlDatabase('banco-teste', user='postgres', password='postgres', host='localhost', port=5432)
#BANCO = PostgresqlDatabase('rinha', user='admin', password='123', host='database', port=5432)

class Cliente(Model):
    nome = CharField(max_length=50)
    limite = IntegerField(null=False)
    class Meta:
        database = BANCO
        table_name = 'clientes'

class Transacao(Model):
    cliente_id = ForeignKeyField(Cliente,backref='transacoes')
    valor = IntegerField(null=False)
    tipo = CharField(max_length=1, null=False)
    descricao = CharField(max_length=10, null=False)
    realizada_em = CharField(max_length=30, null=False)
    class Meta:
        database = BANCO
        table_name = 'transacoes'

class Saldo(Model):
    cliente_id = ForeignKeyField(Cliente,backref='transacoes')
    valor = IntegerField(null=False)
    class Meta:
        database = BANCO
        table_name = 'saldos'


