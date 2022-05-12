import sqlite3 as sql


class ConectaBanco:
    def __init__(self):
        self.__banco = self.__conect()

    @property
    def banco(self):
        return self.__banco

    @property
    def cursor(self):
        return self.banco.cursor()

    def __conect(self):

        try:
            return sql.connect('backup_banco/base_preco.db')
        except Exception as erro:
            raise Exception('Impossível encontar o banco de dados', erro)

    def seleciona_coluna(self, coluna, tabela):
        return self.cursor.execute(f'SELECT {coluna} from {tabela}').fetchall()


if __name__ == '__main__':
    bd = ConectaBanco().banco
