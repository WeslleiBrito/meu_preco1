from datetime import date
# coding: UTF-8

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
            if data_inicial and data_final:
                self.__data_inicial = valida_data(data_inicial)
                if valida_data(data_final) >= date.fromisoformat(str(self.__data_inicial)):
                    self.__data_final = valida_data(data_final)
                else:
                    self.__data_final = data_inicial_padrao()

            elif data_inicial:
                self.__data_inicial = valida_data(data_inicial)
                self.__data_final = str(date.today())

                self.__despesa_fixa = Despesas(data_inicial=self.__data_inicial, data_final=self.__data_final).fixa
                self.__despesa_variavel = Despesas(data_inicial=self.__data_inicial,
                                                   data_final=self.__data_final).variavel
            elif data_final:
                self.__data_inicial = data_inicial_padrao()

                if valida_data(data_final) >= date.fromisoformat(str(self.__data_inicial)):
                    self.__data_final = valida_data(data_final)
                else:
                    self.__data_final = data_inicial_padrao()

                self.__despesa_fixa = Despesas(data_inicial=self.__data_inicial, data_final=self.__data_final).fixa
                self.__despesa_variavel = Despesas(data_inicial=self.__data_inicial,
                                                   data_final=self.__data_final).variavel
            else:
                mes = date.today().month
                ano = date.today().year
                if len(str(mes)) > 1:
                    data = f'{ano}-{mes}-01'
                else:
                    data = f'{ano}-0{mes}-01'

                self.__data_inicial = data
                self.__data_final = str(date.today())

        else:
            self.__data_inicial = data_inicial_padrao()
            self.__data_final = str(date.today())

        self.__despesa_fixa = Despesas(data_inicial=self.__data_inicial, data_final=ultimo_dia_do_mes()).fixa
        self.__despesa_variavel = Despesas(data_inicial=self.__data_inicial, data_final=ultimo_dia_do_mes()).variavel

        self.__faturamento_total = FaturamentoSubgrupo(self.__data_inicial, self.__data_final).faturamento_total
        self.__custo_total = FaturamentoSubgrupo(self.__data_inicial, self.__data_final).custo_total

    @property
    def resumo(self):
        return self.__resumo()

    def __resumo(self):
        import pandas as pd

        dados = dict()

        dados['Faturamento'] = [self.__faturamento_total]
        dados['Custo'] = [self.__custo_total]
        dados['Despesa Fixa'] = [self.__despesa_fixa]
        dados['Despesa Variavel'] = [self.__despesa_variavel]

        dados['Saida total'] = [self.__custo_total + dados['Despesa Fixa'][0] + dados['Despesa Variavel'][0]]

        dados['Lucro R$'] = [round(dados['Faturamento'][0] - (dados['Despesa Fixa'][0] + dados['Custo'][0]), 2)]
        dados['Lucro %'] = [round(dados['Lucro R$'][0] / dados['Faturamento'][0], 3)]
        dados['Margem'] = [round((dados['Faturamento'][0] - dados['Custo'][0]) / dados['Faturamento'][0], 2)]
        dados['Meta Vendas'] = [round(dados['Despesa Fixa'][0] / dados['Margem'][0], 2)]

        if dados['Meta Vendas'][0] > dados['Faturamento'][0]:
            dados['Valor Meta Restante'] = dados['Meta Vendas'][0] - dados['Faturamento'][0]
        else:
            dados['Valor Meta Restante'] = 0.0

        dados['Data Inicial'] = [date.fromisoformat(str(self.__data_inicial)).strftime('%d/%m/%Y')]
        dados['Data Final'] = [date.fromisoformat(str(self.__data_final)).strftime('%d/%m/%Y')]

        return pd.DataFrame(dados)


if __name__ == '__main__':
    print(ResumosLucro().resumo)
