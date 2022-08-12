# coding: UTF-8
from lucratividade import Lucratividade


def espaco_nomes(descricao, valor, limite=25):
    valor = len(str(valor))
    descricao = len(str(descricao))

    return limite - (valor + descricao)


lucros = Lucratividade(comissao=1, data_final='2022-08-11').lucratividade_por_item

faturamento = 0.0
contador = 0
for item in lucros.values():

    faturamento += item['faturamento']
    contador += 1
print(faturamento, contador)

