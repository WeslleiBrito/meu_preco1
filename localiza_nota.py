from tkinter import filedialog


class localizaNotaEntrada:
    def __init__(self, caminho_inicial):
        self.__inicial = caminho_inicial
        self.__arquivo = self.seleciona_arquivo()

    @property
    def arquivo(self):
        return self.__arquivo

    def seleciona_arquivo(self):
        arquivo = filedialog.askopenfilename(title='Localizar nota entrada',
                                             filetypes=(('Arquivo Excel', '*.xlsx'), ('', '')), initialdir=self.__inicial)
        if arquivo:
            return arquivo
        return False


if __name__ == '__main__':
    incial = r'C:\Users\9010\Desktop\Criação de preços'
    arquivo = localizaNotaEntrada(incial)
    print(arquivo.arquivo)
