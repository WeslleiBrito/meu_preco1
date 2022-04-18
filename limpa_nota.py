import pandas as pd
from tkinter.filedialog import askopenfilename


class LimpaNota(object):
    def __init__(self, path, aba):
        self.path = path
        self.aba = aba
        if self.valida_nota()[0]:
            self.planilha = self.valida_nota()[1]
        else:
            raise Exception('Verifique os dados da nota.')

    def valida_nota(self):
        try:
            pd.read_excel(self.path, self.aba)
        except(TypeError, ValueError):
            return [False]
        else:
            return [True, pd.read_excel(self.path, self.aba)]

    def limpa_nota(self):

        if self.planilha.iloc[2, 0].strip() == 'Filtro:':
            df = self.planilha.drop(index=[0, 1, 2])
        else:
            df = self.planilha.drop(index=[0, 1])

        df = df.drop(df.index[[-1, -2]])

        valores = {'Código': [valor for valor in df['Unnamed: 0'][1:]],
                   'Descricão': [valor for valor in df['Unnamed: 1'][1:]],
                   'Custo': [valor for valor in df['Relatório'][1:]]}

        return pd.DataFrame(valores)


if __name__ == '__main__':
    caminho = askopenfilename(filetypes=(("Arquivo do Excel", "*.xlsx"), ('', '')))

    planilha_limpa = LimpaNota(caminho, 'A').limpa_nota()
    print(planilha_limpa)


