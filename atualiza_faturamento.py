#!/usr/bin/python
# -*- coding: latin-1 -*-

from conecta_banco import BancoDeDados
from dados_planilha import BuscaNaPlanilha
from dados_banco import BuscaDados
from backup_banco import ExecutaBackup

class AtualizaFaturamento:
    def __init__(self):
        self.__planilha = BuscaNaPlanilha()
        self.__dados_banco = BuscaDados()
        self.__banco = BancoDeDados().banco

    @property
    def banco(self):
        return self.__banco

    @property
    def cursor(self):
        return self.banco.cursor()

    @property
    def banco_indice(self):
        return self.__dados_banco.indices

    @property
    def banco_sugrupo(self):
        return self.__dados_banco.subgrupos

    @property
    def banco_quantidade(self):
        return self.__dados_banco.quantidade

    @property
    def banco_custo(self):
        return self.__dados_banco.custo

    @property
    def banco_faturamento(self):
        return self.__dados_banco.faturamento

    @property
    def planilha_subgrupo(self):
        return self.__planilha.subgrupo

    @property
    def planilha_quantidade(self):
        return self.__planilha.quantidade

    @property
    def planilha_custo(self):
        return self.__planilha.custo

    @property
    def planilha_faturamento(self):
        return self.__planilha.faturamento

    def faturamento_custo_totais(self):
        faturamento_total = round(sum([faturamento for faturamento in self.banco_faturamento]))
        custo_total = round(sum(custo for custo in self.banco_custo))

        if self.cursor.execute(f'SELECT indice FROM valores_gerais WHERE indice = 1').fetchall():
            self.cursor.execute(f'UPDATE valores_gerais SET faturamento = {faturamento_total}, custo = {custo_total} WHERE indice = 1')
        else:
            self.cursor.execute(f'INSERT INTO valores_gerais (faturamento, custo) VALUES (?, ?)',
                                (faturamento_total, custo_total))

        self.banco.commit()

    def atualiza(self):
        ExecutaBackup().backup()
        subgrupo_planilha = self.planilha_subgrupo
        subgrupo_banco = self.banco_sugrupo
        quantidade_planilha = self.planilha_quantidade
        quantidade_banco = self.banco_quantidade
        indices_banco = self.banco_indice
        custo_planilha = self.planilha_custo
        custo_banco = self.banco_custo
        faturamento_planilha = self.planilha_faturamento
        faturamento_banco = self.banco_faturamento

        for indice, subgrupo in enumerate(subgrupo_banco):
            if subgrupo in subgrupo_planilha:
                indice_planilha = subgrupo_planilha.index(subgrupo)
                total_quantidade = quantidade_planilha[indice_planilha] + quantidade_banco[indice]
                total_custo = custo_planilha[indice_planilha] + custo_banco[indice]
                total_faturamento = faturamento_planilha[indice_planilha] + faturamento_banco[indice]

                self.cursor.execute(
                    f'UPDATE base_despesa_fixa SET quantidade = {total_quantidade}, custo = {total_custo},'
                    f' faturamento = {total_faturamento} WHERE indice = {indices_banco[indice]}')

        self.banco.commit()



if __name__ == '__main__':
    AtualizaFaturamento().faturamento_custo_totais()
