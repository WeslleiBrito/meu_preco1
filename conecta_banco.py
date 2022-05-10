
import sqlite3 as sql

class bancoDeDados:

    def __init__(self):
        self.__banco = self.__conecta()
        self.__cursor = self.__conecta().cursor()

    @property
    def cursor(self):
        return self.__conecta()

    @property
    def banco(self):
        return self.__banco


    def __conecta(self):
        try:
            return sql.connect("base_preco.db")

        except Exception as erro:
            raise Exception('Banco de dados inacessível:', erro)

    def seleciona_tabela(self, nome_tabela):
        return self.cursor.execute(f'SELECT * FROM {nome_tabela}').fetchall()

    def seleciona_coluna(self, tabela, coluna):
        return self.cursor.execute(f'SELECT {coluna} from {tabela}').fetchall()

    def altera_valor(self, tabela, novo_valor, chave_pesquisa):

        return self.cursor.execute(f'')


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
