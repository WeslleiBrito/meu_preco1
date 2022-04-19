import os
import sqlite3 as sql
from tkinter.filedialog import askopenfilename


def caminho(localhost=None):
    with open('caminhos.txt', 'r+') as caminhos:
        if caminhos == '' and localhost is None:
            endereco = askopenfilename(filetypes=(('Arquivo SQlite3', '*.db'), ('', '')))
            if endereco:
                caminhos.write(endereco)
                return caminhos.readline()[0]
            else:
                print('Informe um banco de dados válido!')
        elif localhost is not None:
            return localhost
        return caminhos.readline()[0]


# if not localhost:
#     endereco = askopenfilename(filetypes=(('Arquivo SQlite3', '*.db'), ('', '')))
#     if endereco:
#         with open('camonhos.txt', '') as caminhos:
#             caminhos.write(endereco)
#     return caminhos.readline()[0]
# return localhost


class conectaBanco:

    def __init__(self):
        self.__cursor = self.__conecta()

    def __conecta(self):
        try:
            banco = sql.connect(caminho())
            cursor = banco.cursor()
            return cursor
        except Exception as erro:
            raise Exception('Banco de dados inacessível:', erro)

    def seleciona_tabela(self, nome_tabela):
        return self.__cursor.execute(f'SELECT * FROM {nome_tabela}').fetchall()

    def seleciona_coluna(self, tabela, coluna):
        return self.__cursor.execute(f'SELECT {coluna} from {tabela}').fetchall()


local_arquivo = caminho()

# if __name__ == '__main__':
#     coluna_codigos = conectaBanco().seleciona_coluna('estoque', 'codigo')
#     coluna_subGrupos = conectaBanco().seleciona_coluna('estoque', 'sub_grupo')
#
#     lista_codigos = [codigo[0] for codigo in coluna_codigos]
#     lista_subGrupos = [subGrupo[0] for subGrupo in coluna_subGrupos]
#     print(lista_codigos)
#     if '20002' in lista_codigos:
#         print(lista_subGrupos[lista_codigos.index('20002')])
#     else:
#         print('Não')
