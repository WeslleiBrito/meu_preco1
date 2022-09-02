from lucratividade import Lucratividade

lc_geral = Lucratividade(comissao=1, data_inicial='2022-09-01', data_final='2022-09-01')

lucro_item = lc_geral.lucratividade_por_item

total_lucro = 0.0

for lucro in lucro_item:
    if lucro_item[lucro]['negativo'] < 0:
        total_lucro += lucro_item[lucro]['negativo']
        print(lucro_item[lucro])

print(total_lucro)

