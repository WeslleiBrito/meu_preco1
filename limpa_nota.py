import pandas as pd
from recebe_nota import RecebeNota

class LimpaNota(object):
    def __init__(self):
        self.planilha = RecebeNota().gera_dataframe()

    def __str__(self):
        return f'{self.limpa_nota()}'

    def limpa_nota(self):

        if self.planilha.iloc[2, 0].strip() == 'Filtro:':
            df = self.planilha.drop(index=[0, 1, 2])
        else:
            df = self.planilha.drop(index=[0, 1])

        df = df.drop(df.index[[-1, -2]])

        valores = {'Codigo': [valor for valor in df['Unnamed: 0'][1:]],
                   'Descricao': [valor for valor in df['Unnamed: 1'][1:]],
                   'Custo': [valor for valor in df['Relatório'][1:]]}

        return pd.DataFrame(valores)


if __name__ == '__main__':
    planilha_limpa = LimpaNota()
    print(planilha_limpa)

