
import sqlite3 as sql

class bancoDeDados:

    def __init__(self):
        self.__cursor = self.__conecta()

    @property
    def cursor(self):
        return self.__conecta()

    def __conecta(self):
        try:
            banco = sql.connect(r"C:\Users\9010\PycharmProjects\meu_preco1\base_preco.db")
            cursor = banco.cursor()
            return cursor
        except Exception as erro:
            raise Exception('Banco de dados inacessível:', erro)

    def seleciona_tabela(self, nome_tabela):
        return self.cursor.execute(f'SELECT * FROM {nome_tabela}').fetchall()

    def seleciona_coluna(self, tabela, coluna):
        return self.cursor.execute(f'SELECT {coluna} from {tabela}').fetchall()


if __name__ == '__main__':
    coluna_codigos = bancoDeDados().seleciona_coluna('estoque', 'codigo')
    coluna_subGrupos = bancoDeDados().seleciona_coluna('estoque', 'sub_grupo')

    lista_codigos = [codigo[0] for codigo in coluna_codigos]
    lista_subGrupos = [subGrupo[0] for subGrupo in coluna_subGrupos]
    print(lista_codigos)
    if '20002' in lista_codigos:
        print(lista_subGrupos[lista_codigos.index('20002')])
    else:
        print('Não')
