#!/usr/bin/python
# -*- coding: latin-1 -*-

from conecta_banco import BancoDeDados
from recebe_nota import recebeNota


def atualiza_lista_de_estoque():
    banco = BancoDeDados().banco
    planilha = recebeNota('', 'A').dataframe

    codigo_estoque_sistema = [str(codigo) for codigo in planilha['Código'][0:]]
    descricao_estoque_sistema = [descricao.strip() for descricao in planilha['Descrição'][0:]]
    subgrupo_estoque_sistema = [subgrupo.strip() for subgrupo in planilha['Subgrupo'][0:]]

    codigo_estoque_banco = BancoDeDados().seleciona_coluna('estoque', 'codigo')
    produtos_nao_cadastrados = [codigo for codigo in codigo_estoque_sistema if codigo not in codigo_estoque_banco]

    if len(produtos_nao_cadastrados) > 0:
        for codigo in produtos_nao_cadastrados:
            descricao = descricao_estoque_sistema[codigo_estoque_sistema.index(codigo)]
            subgrupo = subgrupo_estoque_sistema[codigo_estoque_sistema.index(codigo)]
            banco.cursor_sqlite().execute("INSERT INTO estoque (codigo, descricao, sub_grupo) VALUES (?, ?, ?)",
                                          (codigo, descricao, subgrupo))
            print(f'Produto "{descricao}" cadastrado.')
        banco.commit()
        banco.cursor_sqlite().close()
        banco.close()
    else:
        print('Banco já atualizado, nenhum novo produto encontrado.')


atualiza_lista_de_estoque()
