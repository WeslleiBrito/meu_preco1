# coding: UTF-8

from conexao_banco import conecta_banco
from datetime import date
from valores_padroes import data_inicial_padrao


class Despesas:
    def __init__(self, data_inicial=str(data_inicial_padrao()), data_final=str(date.today())):
        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()

        try:
            ano = int(data_inicial[0:4])
            mes = int(data_inicial[5:7])
            dia = int(data_inicial[8:])
            self.__data_inicial = date(ano, mes, dia)

            ano = int(data_final[0:4])
            mes = int(data_final[5:7])
            dia = int(data_final[8:])
            self.__data_final = date(ano, mes, dia)

        except(ValueError, TypeError):
            print('Data inválida')
            raise Exception

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
        self.__cursor.execute(
            f'SELECT rateio_tipoconta, DATE_FORMAT(rateio_dtvencimento,"%d%/%m%/%Y") as Vencimento, rateio_vlrparcela FROM pagar_rateio WHERE rateio_dtvencimento BETWEEN "{self.__data_inicial}" AND "{self.__data_final}";')

        geral = [item for item in self.__cursor.fetchall()]

        tipo_fixa = self.__tipo_despesas()[0]
        tipo_variavel = self.__tipo_despesas()[1]
        valor_despesa_fixa = 0
        valor_despesa_variavel = 0

        for item in geral:
            if item[0] in tipo_fixa:
                valor_despesa_fixa += item[2]
            elif item[0] in tipo_variavel:
                valor_despesa_variavel += item[2]

        return round(valor_despesa_fixa, 2), round(valor_despesa_variavel, 2)


if __name__ == '__main__':
    tipos = Despesas(data_inicial='2022-07-01', data_final='2022-07-31')
    print('Variavel:', tipos.variavel)
    print('Fixa:', tipos.fixa)
