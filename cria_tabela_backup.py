from cria_banco_backup import CriaBanco
from comandos_criacao_tabela import tabelas

class CriaTabela:
    def __init__(self):
        self.__banco = CriaBanco().banco
        self.__tabelas = tabelas

    @property
    def banco(self):
        return self.__banco

    @property
    def tabelas(self):
        return self.__tabelas

    @property
    def cursor(self):
        return self.banco.cursor()

    def criador(self):
        for comando in self.tabelas:
            self.cursor.execute(comando)
        self.banco.commit()


if __name__ == '__main__':
    CriaTabela().criador()
