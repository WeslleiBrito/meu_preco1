from faturamento_subgrupos import FaturamentoSubgrupos
from despesas import Despesas


class DespesaFixaSubgrupo:
    def __init__(self, lista_variavel):
        self.__faturamento = FaturamentoSubgrupos().faturamento_subgrupo
        self.__despesa = Despesas(lista_variavel).despesa_total

    @property
    def total_despesa_sub_grupo(self):
        return self.__calcula_despesa_fixa()

    def __calcula_despesa_fixa(self):
        despesa_subgrupo = dict()
        faturamento_total = sum([venda[0] for venda in self.__faturamento.values()])

        for fatura in self.__faturamento:
            if self.__faturamento[fatura][0] > 0:
                calculo = (self.__faturamento[fatura][0] / faturamento_total) * self.__despesa['Despesa Fixa'] / \
                          self.__faturamento[fatura][1]
                despesa_subgrupo[fatura] = round(calculo, 2)
            else:
                despesa_subgrupo[fatura] = 0.0

        return despesa_subgrupo


if __name__ == '__main__':
    despesas_variaveis = ['FATURAMENTO', 'CMV', 'RH(CMV)', 'RH(CV)', 'TRANSPORTE(CV)', 'TRANSPORTES (CMV)']
    valores = DespesaFixaSubgrupo(despesas_variaveis).total_despesa_sub_grupo

    for item in valores.items():
        print(item)
