from conexao_banco import conecta_banco


class TabelasBanco:
    def __init__(self):
        self.__banco = conecta_banco()

    @property
    def banco(self):
        return self.__banco

    @property
    def faturamento_subgrupo(self):
        return self.__faturamento_subgrupo()

    @property
    def tabela_cadastro_produto(self):
        return self.__tabela_cadastro_produto()

    @property
    def tabela_venda(self):
        return self.__tabela_venda()

    def __tabela_venda(self):
        cursor = self.banco.cursor()

        cursor.execute('SELECT venda, produto, qtd, total, descricao FROM venda_item')
        tabela_venda_item = cursor.fetchall()

        codigo_venda = [cod[1] for cod in tabela_venda_item]
        quantidade_venda = [qtd[2] for qtd in tabela_venda_item]
        total_venda = [total[3] for total in tabela_venda_item]

        return codigo_venda, quantidade_venda, total_venda

    def __tabela_cadastro_produto(self):

        cursor = self.banco.cursor()
        cursor.execute('SELECT prod_cod, prod_dsubgrupo FROM produto')
        tabela_produto = cursor.fetchall()

        codigo_produto = [codigo[0] for codigo in tabela_produto]
        subgrupo_produto = [subgrupo[1] for subgrupo in tabela_produto]

        return codigo_produto, subgrupo_produto

    def __faturamento_subgrupo(self):

        cursor = self.banco.cursor()

        cursor.execute('SELECT venda, produto, qtd, total, descricao FROM venda_item')
        tabela_venda_item = cursor.fetchall()

        codigo_venda = [cod[1] for cod in tabela_venda_item]
        quantidade_venda = [qtd[2] for qtd in tabela_venda_item]
        total_venda = [total[3] for total in tabela_venda_item]

        cursor.execute('SELECT prod_cod, prod_dsubgrupo FROM produto')
        tabela_produto = cursor.fetchall()

        codigo_produto = [codigo[0] for codigo in tabela_produto]
        subgrupo_produto = [subgrupo[1] for subgrupo in tabela_produto]

        faturamento_subgrupo_total = dict()

        for sub in subgrupo_produto:
            faturamento_subgrupo_total[sub] = [0.0, 0.0]

        for indice, cdg in enumerate(codigo_venda):
            posicao = codigo_produto.index(cdg)
            faturamento_subgrupo_total[f'{subgrupo_produto[posicao]}'][0] += \
                total_venda[indice]
            faturamento_subgrupo_total[f'{subgrupo_produto[posicao]}'][1] += \
                quantidade_venda[indice]

        return faturamento_subgrupo_total


if __name__ == '__main__':
    tabelas = TabelasBanco()

    print(tabelas.faturamento_subgrupo)
