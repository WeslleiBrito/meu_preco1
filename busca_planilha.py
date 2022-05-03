from tkinter import filedialog


class buscaPlanilhaExcel:
    def __init__(self):
        self.__caminho = self.busca()

    @property
    def caminho(self):
        return self.__caminho

    def busca(self):
        return filedialog.askopenfilename(filetypes=(('Arquivo excel', '*.xlsx'), ('', '')))


class buscaPlanilhaCsv:

    def __init__(self):
        self.__caminho = self.busca()

    @property
    def caminho(self):
        return self.__caminho

    def busca(self):
        return filedialog.askopenfilename(filetypes=(('Arquivo excel', '*.csv'), ('', '')))


if __name__ == '__main__':
    arquivo = buscaPlanilhaCsv()
    print(arquivo.caminho)
