from conexao_banco import conecta_banco


class FaturamentoSubgrupo:
    def __init__(self):
        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()

    @property
    def faturamento_por_subgrupo(self):
        return self.__faturamento_subgrupo()

    @property
    def faturamento_total(self):
        return self.__faturamento_total()

    def __soma_produtos(self):
        self.__cursor.execute(
            "SELECT produto, SUM(qtd - qtd_devolvida), SUM(vrcusto_composicao * (qtd - qtd_devolvida)), SUM(desconto), SUM(total), SUM(qtd_devolvida)  FROM venda_item GROUP BY descricao ORDER BY total DESC;")

        valores = self.__cursor.fetchall()

        return [(dados[0], dados[1], dados[2], float(dados[3]), float(dados[4]), dados[5]) for dados in valores]

    def __lista_subgrupos(self):
        self.__cursor.execute('SELECT subprod_descricao FROM subgrupo_produtos')

        return [descricao[0] for descricao in self.__cursor.fetchall()]

    def __faturamento_subgrupo(self):
        self.__cursor.execute("SELECT prod_cod, prod_dsubgrupo FROM produto")

        codigo_subgrupo = self.__cursor.fetchall()
        codigos = [cod[0] for cod in codigo_subgrupo]
        subgrupo_lista = [sub[1] for sub in codigo_subgrupo]

        subgrupo = dict()

        for nome in self.__lista_subgrupos():
            subgrupo[nome] = {'quantidade': 0.0, 'custo': 0.0, 'desconto': 0.0,
                              'faturamento': 0.0, 'qtd_devolvida': 0.0}

        for item in self.__soma_produtos():
            chave = subgrupo_lista[codigos.index(item[0])]
            subgrupo[chave]['quantidade'] += item[1]
            subgrupo[chave]['custo'] += item[2]
            subgrupo[chave]['desconto'] += item[3]
            subgrupo[chave]['faturamento'] += item[4]
            subgrupo[chave]['qtd_devolvida'] += item[5]

        return subgrupo

    def __faturamento_total(self):
        geral = self.__faturamento_subgrupo()
        return sum([geral[item]['faturamento'] for item in geral])


if __name__ == '__main__':
    fatura = FaturamentoSubgrupo()
    print(fatura.faturamento_por_subgrupo)
