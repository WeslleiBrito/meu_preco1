# coding: UTF-8

from conexao_banco import conecta_banco
from datetime import date
from valores_padroes import data_inicial_padrao
from validador import valida_data


class Despesas:
    def __init__(self, data_inicial=valida_data(data_inicial_padrao()), data_final=valida_data(str(date.today()))):
        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()
        self.__data_inicial = data_inicial
        self.__data_final = data_final

    @property
    def variavel(self):
        return self.__calcula_despesas()[1]

    @property
    def fixa(self):
        return self.__calcula_despesas()[0]

    @property
    def lista(self):
        return self.__lista

    def __tipo_despesas(self):
        self.__cursor.execute('SELECT tipocont_cod, tipocont_despesa, conta_fixa FROM tipoconta')

        tipo_geral = self.__cursor.fetchall()

        tipo_fixa = [cod_despesa[0] for cod_despesa in tipo_geral if cod_despesa[2] != 0]
        tipo_variavel = [cod_despesa[0] for cod_despesa in tipo_geral if cod_despesa[2] == 0 and cod_despesa[1] != 10]

        return tipo_fixa, tipo_variavel

    def __soma(self, valor):

        return sum([item[0] for item in valor])
    
    def __calcula_despesas(self):
        query_variavel = f"""
            SELECT
            pagar_rateio.rateio_vlrparcela AS "Valor da Parcela"
            FROM
            tipoconta
            INNER JOIN pagar_rateio ON pagar_rateio.rateio_tipoconta = tipoconta.tipocont_cod WHERE pagar_rateio.rateio_dtvencimento BETWEEN "{self.__data_inicial}" AND "{self.__data_final}"  AND tipoconta.conta_fixa = 0 AND tipoconta.tipocont_cod <> 79 AND tipoconta.tipocont_cod <> 75; 

        """

        query_fixa = f"""
            SELECT
            pagar_rateio.rateio_vlrparcela AS "Valor da Parcela"
            FROM
            tipoconta
            INNER JOIN pagar_rateio ON pagar_rateio.rateio_tipoconta = tipoconta.tipocont_cod WHERE pagar_rateio.rateio_dtvencimento BETWEEN "{self.__data_inicial}" AND "{self.__data_final}"  AND tipoconta.conta_fixa = 1; 

        """

        self.__cursor.execute(query_variavel) 
        variavel = self.__soma(self.__cursor.fetchall())
        self.__cursor.execute(query_fixa)
        fixa = self.__soma(self.__cursor.fetchall())

        return round(fixa, 2), round(variavel, 2)

    


if __name__ == '__main__':
    tipos = Despesas(data_inicial='2023-06-01', data_final='2023-06-30')
    print('Variavel:', tipos.variavel, "\n" + 'Fixa:', tipos.fixa)