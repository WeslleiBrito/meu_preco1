import sqlite3
from datetime import datetime


class CriaBanco:
    def __init__(self):
        self.__data = datetime.now()

    @property
    def data(self):
        return self.__data_convertida()

    @property
    def banco(self):
        return self.__cria_banco()

    def __data_convertida(self):
        return str(self.__data).replace('.', '-').replace(':', '-')

    def __cria_banco(self):
        return sqlite3.connect(f'backup_banco/base_preco{self.data}.db')


if __name__ == '__main__':
    db = CriaBanco().banco
