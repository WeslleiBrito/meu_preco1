from conexao_banco import conecta_banco
import pandas as pd


class Faturamento:
    def __init__(self):
        self.__banco = conecta_banco()

    @property
    def cursor(self):
        return self.__banco.cursor_sqlite()

    @property
    def total(self):
        return self.__total()

    @property
    def subgrupos(self):
        return self.__subgrupos()

    @property
    def calculador_subgrupo_despesa(self):
        return self.__calculador_subgrupo_despesa()

    @property
    def faturamento(self):
        return self.__faturamento_geral()

    @property
    def produto_subgrupo(self):
        return self.__produto_subgrupo()

    @property
    def agrupa_codigo_por_subgrupo(self):
        return self.__agrupa_codigo_por_subgrupo()

    @property
    def faturamento_subgrupos(self):
        return self.__calculador_valor_subgrupos()

    @property
    def faturamento_produto(self):
        return self.__faturamento_produto_quantidade()

    def __total(self):
        dados = {'venda': [], 'codigo': [], 'descricao': [], 'quantidade': [], 'total': []}
        cursor = self.cursor
        cursor.execute('SELECT venda, produto, qtd, total, descricao FROM venda_item')

        for item in cursor.fetchall():
            dados['venda'].append(item[0])
            dados['codigo'].append(item[1])
            dados['quantidade'].append(item[2])
            dados['total'].append(item[3])
            dados['descricao'].append(item[4])

        return pd.DataFrame(dados, index=None).sort_values(by='codigo')

    def __faturamento_geral(self):

        return round(sum(self.total['total']), 2)

    def __subgrupos(self):
        cursor = self.cursor
        cursor.execute('SELECT prod_dsubgrupo FROM produto')

        return set([sub[0] for sub in cursor.fetchall()])

    def __produto_subgrupo(self):
        cursor = self.cursor
        cursor.execute('SELECT prod_cod, prod_dsubgrupo FROM produto')

        return cursor.fetchall()

    def __agrupa_codigo_por_subgrupo(self):
        subgrupo = dict()

        for chave in self.subgrupos:
            subgrupo[chave] = []

        for item in self.produto_subgrupo:
            if item[1] in subgrupo.keys():
                subgrupo[item[1]].append(item[0])

        return subgrupo

    def __calculador_valor_subgrupos(self):

        return self.faturamento

    def __faturamento_produto_quantidade(self):
        fat_produto = dict()
        total = self.total
        valor_temp = 0.0
        qtd_temp = 0.00

        codigo_all = total['codigo']
        codigo_unico = set(codigo_all)
        quantidade = [qtd for qtd in total['quantidade']]
        total = [tl for tl in total['total']]

        for chave in codigo_unico:
            for indice, codigo_avalia in enumerate(codigo_all):
                if chave == codigo_avalia:
                    valor_temp += total[indice]
                    qtd_temp += quantidade[indice]

            fat_produto[str(chave)] = round(valor_temp, 2), qtd_temp
            valor_temp = 0.0
            qtd_temp = 0.00

        return fat_produto


if __name__ == '__main__':
    teste = Faturamento()

    for item in teste.faturamento_produto.items():
        print(item)

    print(len(teste.agrupa_codigo_por_subgrupo.keys()))


