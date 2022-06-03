from limpa_nota_de_entrada import LimpaNotaEntrada
from conecta_banco import BancoDeDados

class BuscaValores:
    def __init__(self):
        self.__planilha = LimpaNotaEntrada()

    @property
    def planilha(self):
        return self.__planilha.limpaPlanilha()

    def coleta_dados(self):

        if self.planilha:
            return self.planilha


if __name__ == '__main__':
    print(BuscaValores().coleta_dados())

