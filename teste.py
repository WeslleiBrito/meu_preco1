from busca_planilha import BuscaPlanilhaExcel
import pandas as pd


class CriaDataFrameDespesa:
    def __init__(self):
        self.__caminho = BuscaPlanilhaExcel().caminho

    @property
    def planilha(self):
        return self.__limpeza_planilha()

    def __data_frame(self):
        return pd.read_excel(self.__caminho, 'A')

    def __limpeza_planilha(self):
        planilha = self.__data_frame()
        planilha.drop(columns=['Unnamed: 5', 'Unnamed: 6'], inplace=True)
        planilha.columns = ['Despesas', 'Registros', 'Valor', 'Pago', 'A pagar']
        planilha = planilha.dropna()
        planilha = planilha.drop(planilha.index[[0, -1]])

        for despesa in planilha['Despesas']:
            if despesa == '10 - FATURAMENTO':
                indice_faturamento = planilha[planilha['Despesas'] == '10 - FATURAMENTO'].index
                planilha.drop(index=indice_faturamento, inplace=True)

        return planilha


if __name__ == '__main__':
    pl = CriaDataFrameDespesa().planilha
    print(pl)


