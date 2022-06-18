#!/usr/bin/python
# -*- coding: latin-1 -*-

import mysql.connector


config = {'host': '192.168.15.13',
          'database': 'clarionerp',
          'user': 'burite',
          'password': 'burite123',
          'port': '3307'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

cursor.execute('SELECT DATE_FORMAT(rateio_dt_pagamento,"%d%/%m%/%Y"), rateio_tipodesp, rateio_tpdespesanome,'
               ' rateio_vlr_pagamento FROM pagar_rateio')


lista_des_variavel = [2, 22, 23]

despesas = [dados for dados in cursor.fetchall() if dados[0]]

despesa_fixa = 0.0
despesa_variavel = 0.0


for d in despesas:
    if d[0]:
        if d[1] not in lista_des_variavel and d[1] != 10:
            if d[3]:
                despesa_fixa += d[3]
        elif d[1] in lista_des_variavel and d[1] != 10:
            if d[3]:
                despesa_variavel += d[3]


print(f'Despesa Fixa: {round(despesa_fixa)} / Despesa variável: {round(despesa_variavel)}')

cursor.execute('SELECT venda, produto, qtd, total, descricao FROM venda_item')
tabela_all = [valor for valor in cursor.fetchall()]

codigos = set([codigo[1] for codigo in tabela_all])
cd_r = [codigo[1] for codigo in tabela_all]
quantidade = [quantidade[2] for quantidade in tabela_all]
total = [total[3] for total in tabela_all]
produtos = [descricao[4] for descricao in tabela_all]
qtd = 0.0
faturamento_total = round(sum([vr[3] for vr in tabela_all]))
faturamento_produto = 0.0

nome = ''

cursor.execute('SELECT prod_cod, prod_dsubgrupo FROM produto')
geral = [gr for gr in cursor.fetchall()]
tbl_cod_produtos = [cod[0] for cod in geral]
sub_grupos = [sub[1] for sub in geral]

dict_subgrupo = dict()

for sub in sub_grupos:
    dict_subgrupo[f'{sub}'] = []

for chave in dict_subgrupo.keys():
    for indi, sub_grupo_a in enumerate(sub_grupos):
        if chave == sub_grupo_a:
            dict_subgrupo[f'{chave}'].append(tbl_cod_produtos[indi])

dict_valor_subgrupo = dict()

soma = 0.0
for ch in dict_subgrupo.keys():
    for posicao, cd in enumerate(cd_r):
        if cd in dict_subgrupo[f'{ch}']:
            soma += total[posicao]

    dict_valor_subgrupo[f'{ch}'] = soma
    soma = 0.0

for vr_sub in dict_valor_subgrupo.items():
    print(vr_sub)

# for codigo in codigos:
#     for index, dados in enumerate(tabela_all):
#         if dados[1] == codigo:
#             qtd += quantidade[index]
#             faturamento_produto += total[index]
#             nome = produtos[index]
#
#     dps = round(((faturamento_produto / faturamento_total) * despesa_fixa) / qtd, 2)
#     print(f'Codigo: {codigo}, Quantidade: {qtd} Nome: {nome}, Total: {faturamento_produto}, Despesa Fixa: {dps}')
#     faturamento_produto = 0.0
#     qtd = 0.0
#
# print(faturamento_total)

conn.close()





