# coding: UTF-8
from datetime import date
from validador import ultimo_dia_do_mes


class ResumosLucro:

    def __init__(self, data_inicial='', data_final='', geral=False):
        """

        :param data_inicial: Por padrão é sempre uma string vazia, já que nessa condição a data inicial será sempre
        o primeiro dia do mês atual
        :param data_final: já data atual será vazia
        :param geral: Caso geral seja false ele considera as datas padrões, do contrário vai ser utilizado a data inicial
        como primeira movimentação do banco e a data atual da consulta.
        """
        from validador import valida_data, ultimo_dia_do_mes
        from despesas import Despesas
        from faturamento_subgrupos import FaturamentoSubgrupo

        from valores_padroes import data_inicial_padrao

        if geral is False:
            if not data_inicial and not data_final:
                mes = date.today().month
                ano = date.today().year
                if len(str(mes)) > 1:
                    data = f'{ano}-{mes}-01'
                else:
                    data = f'{ano}-0{mes}-01'

                self.__data_inicial = data
                self.__data_final = str(ultimo_dia_do_mes())
            elif data_inicial and not data_final:
                self.__data_inicial = valida_data(data_inicial)
                self.__data_final = str(date.today())
            elif data_final and not data_inicial:
                self.__data_inicial = data_inicial_padrao()
                self.__data_final = valida_data(data_final)
                if self.__data_inicial < valida_data(data_final):
                    self.__data_final = valida_data(data_final)
                    self.__data_inicial = self.__data_final
            elif data_inicial and data_final:
                self.__data_inicial = valida_data(data_inicial)
                self.__data_final = valida_data(data_final)

        self.__despesa_fixa = Despesas(
            data_inicial=self.__data_inicial, data_final=self.__data_final).fixa
        self.__despesa_variavel = Despesas(
            data_inicial=self.__data_inicial, data_final=self.__data_final).variavel

        self.__faturamento_total = FaturamentoSubgrupo(
            self.__data_inicial, self.__data_final).faturamento_total
        self.__custo_total = FaturamentoSubgrupo(
            self.__data_inicial, self.__data_final).custo_total
        print('Data inicial:', self.__data_inicial)
        print('Data final:', self.__data_final)
    @property
    def resumo(self):
        return self.__resumo()

    @property
    def despesa_fixa(self):
        return self.__despesa_fixa

    def __resumo(self):
        from representa_despesa import DespesaSubgrupo
        porcentagem_variavel_global = DespesaSubgrupo().despesa_variavel

        import pandas as pd

        dados = dict()
        dados['Faturamento Real'] = self.__faturamento_total
        dados['Faturamento'] = round(
            self.__faturamento_total * (1 - porcentagem_variavel_global), 2)
        dados['Custo'] = float(self.__custo_total)
        dados['Despesa Fixa'] = float(self.__despesa_fixa)

        dados['Saida total'] = self.__custo_total + dados['Despesa Fixa']

        dados['Lucro R$'] = round(
            dados['Faturamento'] - (dados['Despesa Fixa'] + dados['Custo']), 2)
        dados['Lucro %'] = round(
            (dados['Lucro R$'] / dados['Faturamento']) * 100, 3)
        dados['Margem Real'] = round(
            ((dados['Faturamento Real'] - dados['Custo']) / dados['Faturamento Real']) * 100, 2)
        dados['Margem'] = round(
            (dados['Faturamento'] - dados['Custo']) / dados['Faturamento'], 2)
        dados['Meta Vendas'] = round(
            dados['Despesa Fixa'] / dados['Margem'], 2)

        if dados['Meta Vendas'] > dados['Faturamento']:
            dados['Valor Meta Restante'] = round(
                dados['Meta Vendas'] - dados['Faturamento'], 2)
        else:
            dados['Valor Meta Restante'] = 0.0

        dados['Data Inicial'] = date.fromisoformat(
            str(self.__data_inicial)).strftime('%d/%m/%Y')
        dados['Data Final'] = date.fromisoformat(
            str(self.__data_final)).strftime('%d/%m/%Y')

        return dados


if __name__ == '__main__':
    print(ResumosLucro(data_inicial="2023-06-01", data_final="2023-06-30").resumo)
