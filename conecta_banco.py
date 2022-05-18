import sqlite3 as sql


class BancoDeDados:

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
            return sql.connect(r"\\CAIXABURITE-PC\Users\Public\base_preco.db")
        except Exception as erro:
            raise Exception('Banco de dados inacessível:', erro)

    def seleciona_tabela(self, nome_tabela):
        return self.cursor.execute(f'SELECT * FROM {nome_tabela}').fetchall()

    def seleciona_coluna(self, tabela, coluna):
        return self.cursor.execute(f'SELECT {coluna} from {tabela}').fetchall()


if __name__ == '__main__':
    coluna_codigos = BancoDeDados().seleciona_coluna('despesas_totais', 'descricao')
    coluna_subGrupos = BancoDeDados().seleciona_coluna('despesas_totais', 'valor')

    lista_codigos = [codigo[0] for codigo in coluna_codigos]
    lista_subGrupos = [subGrupo[0] for subGrupo in coluna_subGrupos]
    print(lista_codigos)
    print(lista_subGrupos)
    if '20002' in lista_codigos:
        print(lista_subGrupos[lista_codigos.index('20002')])
    else:
        print('Não')
