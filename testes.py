import timeit
from database import queries as qr
from database import queries_not_async as qrn

rangs = range(1, 200)
# Função não assíncrona
def teste_not_async():
    ids = rangs
    for id in ids:
        qrn.fazer_transacao(id, 100, 'd', f'teste:{id}')

# Função assíncrona
def teste_async():
    ids = rangs
    for id in ids:
        qr.fazer_transacao(id, 100, 'd', f'teste:{id}')

# Executar o teste não assíncrono
execucao1 = timeit.timeit(teste_not_async, number=1)
#print(teste_not_async())
print(f"Tempo teste1 = {execucao1}")

# Executar o teste assíncrono
execucao2 = timeit.timeit(teste_async, number=1)
#print(run_teste_async())
print(f"Tempo teste2 = {execucao2}")

