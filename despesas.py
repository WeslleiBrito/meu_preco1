# coding: UTF-8

from conexao_banco import conecta_banco
from datetime import date

class Despesas:
    def __init__(self):
        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()

    @property
    def variavel(self):
        return self.__calcula_despesas()[1]

    @property
    def fixa(self):
        return self.__calcula_despesas()[0]



    def __tipo_despesas(self):
        self.__cursor.execute('SELECT tipocont_cod, tipocont_despesa, conta_fixa FROM tipoconta')

        tipo_geral = self.__cursor.fetchall()

        tipo_fixa = [cod_despesa[0] for cod_despesa in tipo_geral if cod_despesa[2] != 0]
        tipo_variavel = [cod_despesa[0] for cod_despesa in tipo_geral if cod_despesa[2] == 0 and cod_despesa[1] != 10]

        return tipo_fixa, tipo_variavel

    def __calcula_despesas(self):
        vigentes = []
        self.__cursor.execute(
            'SELECT rateio_tipoconta, DATE_FORMAT(rateio_dt_pagamento,"%d%/%m%/%Y"), rateio_vlrparcela FROM pagar_rateio')

        geral = self.__cursor.fetchall()
        for item in geral:

            data_tabela = item[1]
            if data_tabela:
                data = date(day=int(data_tabela[0:2]), month=int(data_tabela[3:5]), year=int(data_tabela[6:]))

                if data <= date.today():
                    vigentes.append(item)

        tipo_fixa = self.__tipo_despesas()[0]
        tipo_variavel = self.__tipo_despesas()[1]
        valor_despesa_fixa = 0
        valor_despesa_variavel = 0

        for item in vigentes:
            if item[0] in tipo_fixa:
                valor_despesa_fixa += item[2]
            elif item[0] in tipo_variavel:
                valor_despesa_variavel += item[2]

        return round(valor_despesa_fixa, 2), round(valor_despesa_variavel, 2)


if __name__ == '__main__':
    tipos = Despesas()
    print(tipos.variavel)
