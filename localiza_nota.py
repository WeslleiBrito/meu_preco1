from tkinter import filedialog


class LocalizaNotaEntrada:
    def __init__(self, caminho_inicial=''):
        self.__inicial = caminho_inicial
        self.__caminho = self.seleciona_caminho_nota_entrada()

    @property
    def caminho(self):
        return self.__caminho

    def seleciona_caminho_nota_entrada(self):

        return filedialog.askopenfilename(title='Localizar nota entrada',
                                          filetypes=(('Arquivo Excel', '*.xlsx'), ('', '')),
                                          initialdir=self.__inicial)


if __name__ == '__main__':
    inicial = r'C:\Users\9010\Desktop\Criação de preços'
    arquivo = LocalizaNotaEntrada(inicial)
    print(arquivo.caminho)
