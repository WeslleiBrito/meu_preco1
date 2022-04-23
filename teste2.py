import pandas as pd
from localiza_nota import localizaNotaEntrada


class recebeNota:
    def __init__(self, abertura, nome_aba='A'):
        self.__caminho_inicial = abertura
        self.__aba = nome_aba
        self.__caminho_arquivo = self.busca_caminho()

    @property
    def caminho_inicial(self):
        return self.__caminho_inicial

    @property
    def aba(self):
        return self.__aba

    @property
    def caminho_arquivo(self):
        return self.__caminho_arquivo

    @property
    def dataframe(self):
        return self.__gera_dataframe()

    def busca_caminho(self):
        return localizaNotaEntrada(self.caminho_inicial).arquivo

    def __gera_dataframe(self):
        if self.caminho_arquivo:
            return pd.read_excel(self.caminho_arquivo, self.aba)


if __name__ == '__main__':
    inicial = r'C:\Users\9010\Desktop\Criação de preços'
    planilha = recebeNota(inicial, 'A')
    print(planilha.dataframe)
