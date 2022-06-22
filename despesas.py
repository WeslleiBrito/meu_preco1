from conexao_banco import conecta_banco


class Despesas:

    def __init__(self, lista_variavel):
        self.__banco = conecta_banco()
        self.__ls_variavel = lista_variavel

    @property
    def banco(self):
        return self.__banco

    @property
    def cursor(self):
        return self.banco.cursor()

    @property
    def despesa_total(self):
        return self.__despesa_total()

    def __despesa_total(self):
        cr = self.cursor
        cr.execute('SELECT DATE_FORMAT(rateio_dt_pagamento,"%d%/%m%/%Y"), rateio_tipodesp, '
                   'rateio_tpdespesanome, '
                   ' rateio_vlr_pagamento FROM pagar_rateio')
        total = cr.fetchall()
        cr.close()
        return [despesa for despesa in total]

    def separador_despesas(self):

        despesa_variavel = 0.0
        despesa_fixa = 0.0

        tipo_all = []

        despesa_all = self.__despesa_total()

        for tipo in despesa_all:
            if tipo[1] != 10:
                tipo_all.append(str(tipo[1]))

        tipo_all = set(tipo_all)

        for cod_despesa in tipo_all:
            for despesa in despesa_all:
                if str(despesa[1]) == cod_despesa and despesa[1] in self.__ls_variavel and despesa[3] and despesa[
                    0] is not None:
                    despesa_variavel += despesa[3]
                else:
                    if despesa[1] != 10 and despesa[3] and despesa[0] is not None:
                        despesa_fixa += despesa[3]

        return round(despesa_fixa, 2), round(despesa_variavel, 2)


if __name__ == '__main__':
    teste = Despesas(lista_variavel=[2, 22, 23])

    print(teste.separador_despesas())
