# coding: UTF-8
from lucratividade import Lucratividade


def espaco_nomes(descricao, valor, limite=25):
    valor = len(str(valor))
    descricao = len(str(descricao))

    return limite - (valor + descricao)


lucros = Lucratividade(comissao=1).lucratividade_por_item

for info in lucros.items():
    print(info)

custo = 0.0
faturamento = 0.0
despesa_vr = 0.0
comissao = 0.0
fixa = 0.0
negativos = 0.0

for item in lucros:
    custo += lucros[item]['custo']
    faturamento += lucros[item]['faturamento']
    despesa_vr += lucros[item]['despesa variavel']
    comissao += lucros[item]['comissao']
    fixa += lucros[item]['despesa fixa']
    negativos += lucros[item]['negativo']

custo_total = round(custo + despesa_vr + comissao + fixa, 2)
lucro = round(faturamento - custo_total, 2)
porcentagem = round(lucro / faturamento, 2) * 100

nome = ['Faturamento', 'Custo', 'Despesa Variavel', 'Despesa Fixa', 'Comissão', 'Custo total', 'Lucro/Prejuízo',
        'Porcentagem %', 'Prejuízos']
valores = [round(faturamento, 2), round(custo, 2), round(despesa_vr, 2), round(fixa, 2), round(comissao, 2),
           round(custo_total, 2), round(lucro, 2), round(porcentagem, 2), round(negativos, 2)]

print()
for n, v in zip(nome, valores):
    print(f'{n} {espaco_nomes(n, v) * "-"} {v}')
