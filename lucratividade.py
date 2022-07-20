from datetime import date
from conexao_banco import conecta_banco
from rateio_despesa_fixa import DespesasRateio


class Lucratividade:

    def __init__(self, data_inicial=date.today(), data_final=date.today(), comissao=0.0):

        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()
        self.__data_inicial = data_inicial
        self.__data_final = data_final

        if comissao == 0.0:
            self.__comissao = comissao
        else:
            self.__comissao = round(comissao / 100, 2)

    @property
    def datas(self):
        return f'Data Inicial: {self.__data_inicial} - Data Final: {self.__data_final}'

    @property
    def dados_vendas(self):
        return self.__venda_completo()

    @property
    def codigo_subgrupo(self):
        return self.__codigo_subgrupo()

    def __dados_vendas(self):
        dados_vendas = []
        comando = f'SELECT produto, descricao, SUM(qtd - qtd_devolvida) as quantidade, ' \
                  f'SUM(vrcusto_composicao * (qtd - qtd_devolvida)) as custo, SUM(desconto) as desconto, ' \
                  f'SUM(total) as faturamento, SUM(qtd_devolvida) as quantidade_devolvida FROM venda_item ' \
                  f'WHERE dtvenda BETWEEN "{self.__data_inicial}" AND "{self.__data_final}" GROUP BY descricao ORDER BY total DESC;'

        self.__cursor.execute(comando)

        for item in self.__cursor.fetchall():
            dados_vendas.append({'codigo': item[0],
                                 'descricao': item[1],
                                 'quantidade': item[2],
                                 'custo': item[3],
                                 'desconto': float(item[4]),
                                 'faturamento': float(item[5]),
                                 'qtd_devolvilda': item[6]
                                 })

        return dados_vendas

    def __codigo_subgrupo(self):
        self.__cursor.execute('SELECT prod_cod, prod_dsubgrupo FROM produto')
        dados = self.__cursor.fetchall()

        codigo = [item[0] for item in dados]
        subgrupo = [item[1] for item in dados]

        return codigo, subgrupo

    def __venda_completo(self):
        despesa_fixa = DespesasRateio().despesa_fixa
        despesa_variavel = DespesasRateio().despesa_variavel

        codigo = self.__codigo_subgrupo()[0]
        subgrupo = self.__codigo_subgrupo()[1]
        dados_vendas = self.__dados_vendas()

        for indice, item in enumerate(self.__dados_vendas()):
            posicao = codigo.index(item['codigo'])
            fixa = item['quantidade'] * despesa_fixa[subgrupo[posicao]]
            variavel = round(item['faturamento'] * despesa_variavel, 2)
            comissao = round(item['faturamento'] * self.__comissao, 2)

            dados_vendas[indice]['comissao'] = comissao
            dados_vendas[indice]['despesa_variavel'] = variavel
            dados_vendas[indice]['despesa_fixa'] = fixa
            dados_vendas[indice]['custo_total'] = round(dados_vendas[indice]['custo'] + comissao + variavel + fixa, 2)
            dados_vendas[indice]['lucro'] = round(dados_vendas[indice]['faturamento'] - dados_vendas[indice]['custo_total'], 2)
            dados_vendas[indice]['porcentagem_lucro'] = round(dados_vendas[indice]['lucro'] / dados_vendas[indice]['faturamento'], 2)

        return dados_vendas


if __name__ == '__main__':
    print(Lucratividade(comissao=1).dados_vendas)
