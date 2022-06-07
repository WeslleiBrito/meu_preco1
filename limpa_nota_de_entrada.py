# -*- coding: latin-1 -*-

import pandas as pd
from correcao_aba_excel import salva_arquivo_corretamente
from busca_planilha import BuscaPlanilhaExcel


class LimpaNotaEntrada(object):

    def __init__(self):

        self.__caminho = self.__nota_selecionada()

    def __nota_selecionada(self):
        caminho = BuscaPlanilhaExcel().caminho

        if caminho:
            return caminho
        else:
            return False
    @property
    def caminho(self):
        return self.__caminho

    def limpaPlanilha(self):
        caminho = self.caminho

        if caminho:

            salva_arquivo_corretamente(caminho)

            planilha_bruta = pd.read_excel(caminho, sheet_name='A')

            if planilha_bruta.iloc[2, 0].strip() == 'Filtro:':
                planilha_editada = planilha_bruta.drop(index=[0, 1, 2], columns=['Unnamed: 10', 'Unnamed: 11'])
            else:
                planilha_editada = planilha_bruta.drop(index=[0, 1], columns=['Unnamed: 10', 'Unnamed: 11'])

            indices = list()

            for posicao in range(0, 10):
                indices.append(planilha_editada.iat[0, posicao])

            planilha_editada.columns = indices

            planilha_editada = planilha_editada.drop(planilha_editada.index[[0, -1, -2]])

            planilha_limpa = planilha_editada.drop(['Und', 'Fração', 'Vr. Compra', 'Vr. Venda', 'Vr. Compra Novo',
                                                    'Margem', 'Vr. Venda Novo'], axis=1)

            return planilha_limpa


if __name__ == '__main__':
    plan = LimpaNotaEntrada().limpaPlanilha()
    print(plan)
