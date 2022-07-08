#!/usr/bin/python
# -*- coding: latin-1 -*-

import pandas as pd
from busca_planilha import BuscaPlanilhaExcel
from conecta_banco import BancoDeDados
from backup_banco import ExecutaBackup

def define_tipo_despesa_retorna_as_despesas():
    caminho = BuscaPlanilhaExcel().caminho
    pasta = input('Informe o nome da pasta de consulta: ')
    despesas_nao_localizadas = []
    while True:
        escolha = input(f'Escolha o código da despesa [1 - Fixa, 2 - Variável]: ')
        if escolha.isdigit():
            if 0 < int(escolha) <= 2:
                escolha = int(escolha)
                break
            else:
                print('Escolha inválida')
        else:
            print('Informe apenas números inteiro')
    planilha = pd.read_excel(caminho, pasta)

    for codigo, descricao in enumerate(planilha['Descrição']):
        if descricao[0:1].isdigit():
            dps = f'{descricao.strip()}'
        else:
            dps = f'{descricao.strip()}'

        despesas_nao_localizadas.append(dps)
    return despesas_nao_localizadas, escolha


class ImportaDespesas:

    def __init__(self):
        funcao = define_tipo_despesa_retorna_as_despesas()
        self.__despesas = funcao[0]
        self.__tipo_despesa = funcao[1]
        self.__banco = BancoDeDados().banco

    def atualiza_cadastro_despesas(self):
        tipo = 'Fixa'
        if self.__tipo_despesa == 2:
            tipo = 'Variável'

        tabela = [descricao[0] for descricao in self.__banco.cursor_sqlite().execute('SELECT descricao FROM despesas_totais WERE').fetchall()]

        for despesa in self.__despesas:
            if despesa not in tabela:
                self.__banco.cursor_sqlite().execute('INSERT INTO despesas_totais (descricao, tipo_despesa) VALUES (?, ?)', (despesa, tipo))

        self.__banco.commit()
        self.__banco.cursor_sqlite().close()
        self.__banco.close()


if __name__ == '__main__':
    ExecutaBackup().backup()
    ImportaDespesas().atualiza_cadastro_despesas()
