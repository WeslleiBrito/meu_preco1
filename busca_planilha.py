from tkinter import filedialog
from correcao_aba_excel import salva_arquivo_corretamente


class BuscaPlanilhaExcel:
    def __init__(self):
        self.__caminho = self.busca()

    @property
    def caminho(self):
        return self.__caminho

    def busca(self):
        caminho = filedialog.askopenfilename(filetypes=(('Arquivo excel', '*.xlsx'), ('', '')))
        salva_arquivo_corretamente(caminho)
        return caminho


class buscaPlanilhaCsv:

    def __init__(self):
        self.__caminho = self.busca()

    @property
    def caminho(self):
        return str(self.__caminho)

    def busca(self):
        return filedialog.askopenfilename(filetypes=(('Arquivo excel', '*.csv'), ('', '')))


if __name__ == '__main__':
    arquivo = BuscaPlanilhaExcel()
    print(arquivo.caminho)
