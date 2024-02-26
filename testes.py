import asyncio
import timeit
from database import queries as qr
from database import queries_not_async as qrn

rangs = range(1, 100)
# Função síncrona para chamar a função assíncrona
def run_teste_async():
    asyncio.run(teste_async())

# Função não assíncrona
def teste_not_async():
    ids = rangs
    for id in ids:
        qrn.fazer_transacao(id, 100, 'c', f'teste:{id}')

# Função assíncrona
async def teste_async():
    ids = rangs
    for id in ids:
        await qr.fazer_transacao(id, 100, 'c', f'teste:{id}')

# Executar o teste não assíncrono
execucao1 = timeit.timeit(teste_not_async, number=2)
print(f"Tempo teste1 = {execucao1}")

# Executar o teste assíncrono
execucao2 = timeit.timeit(run_teste_async, number=2)
print(f"Tempo teste2 = {execucao2}")
