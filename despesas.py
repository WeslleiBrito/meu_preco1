from conexao_banco import conecta_banco


class Despesas:

    def __init__(self, lista_variavel):
        self.__banco = conecta_banco()
        self.__ls_variavel = lista_variavel

    @property
    def despesa_total(self):
        return self.__despesa_total()

    def __despesa_total(self):
        cr = self.__banco.cursor()

        cr.execute('SELECT rateio_tpdespesanome, SUM(rateio_vlrpagoparcela) AS soma_despesa FROM pagar_rateio GROUP BY '
                   'rateio_tpdespesanome ORDER BY rateio_vlrpagoparcela DESC;')

        valores = cr.fetchall()
        cr.close()

        fixa = sum([valor[1] for valor in valores if valor[0] not in self.__ls_variavel])
        variavel = sum([vlr[1] for vlr in valores if vlr[0] not in ['FATURAMENTO']]) - fixa

        return {'Despesa Fixa': round(fixa, 2), 'Despesa Variavel': round(variavel, 2)}


if __name__ == '__main__':
    despesas_variaveis = ['FATURAMENTO', 'CMV', 'RH(CMV)', 'RH(CV)', 'TRANSPORTE(CV)', 'TRANSPORTES (CMV)']
    despesas = Despesas(despesas_variaveis).despesa_total

    print(despesas)
