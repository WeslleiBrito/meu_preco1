from lucratividade import Lucratividade

lc_geral = Lucratividade(comissao=1, data_inicial='2022-09-01', data_final='2022-09-01')

lucro_item = lc_geral.vendas

total_lucro = 0.0

for itens, venda in enumerate(lucro_item):
    print(venda)

print(itens + 1)

