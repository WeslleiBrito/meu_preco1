#!/usr/bin/python
# -*- coding: latin-1 -*-

from conexao_banco import conecta_banco

banco = conecta_banco()
cursor = banco.cursor_sqlite()


class Despesas:

    def __init__(self, lista_variavel):
        self.__banco = conecta_banco()
        self.__ls_variavel = lista_variavel

    @property
    def banco(self):
        return self.__banco

    @property
    def cursor(self):
        return self.banco.cursor_sqlite()

    @property
    def despesa_total(self):
        return self.__despesa_total()

    def __despesa_total(self):
        cr = self.cursor
        cr.execute('SELECT DATE_FORMAT(rateio_dt_pagamento,"%d%/%m%/%Y"), rateio_tipodesp, '
                   'rateio_tpdespesanome, '
                   ' rateio_vlr_pagamento FROM pagar_rateio')

        return [despesa for despesa in cr.fetchall()]

    def separador_despesas(self):

        despesa_fixa = dict()
        despesa_variavel = dict([])

        despesa_all = self.__despesa_total()

        for cont, despesa in enumerate(despesa_all):
            if despesa[0]:
                if despesa[1] in self.__ls_variavel and despesa[1] != 10:
                    despesa_variavel[f'{despesa[1]}'] += despesa[3]
                elif despesa[1] != 10:
                    despesa_fixa[f'{despesa[1]}'] += despesa[3]

        return despesa_fixa, despesa_variavel


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

banco.close()
