import sqlite3 as sql
from datetime import datetime

nome_banco_backup = 'backup_banco/base_preco' + str(datetime.now()).replace('.', '-').replace(':', '-') + '.db'


class ExecutaBackup:

    def __init__(self):
        self.__banco_atual = sql.connect('base_preco.db')
        self.__backup_banco = sql.connect(nome_banco_backup)

    def backup(self):
        self.__banco_atual.backup(self.__backup_banco)


if __name__ == '__main__':
    ExecutaBackup().backup()
