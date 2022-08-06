# coding: UTF-8
from datetime import date
from conexao_banco import conecta_banco
from rateio_despesa import DespesasRateio


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

    def __vendedores(self):
        """
        :return: retorna duas lista uma com o código do vendedor e outra com o nome
        """
        self.__cursor.execute('SELECT fun_cod,  fun_nome FROM funcionario;')
        dados = self.__cursor.fetchall()
        codigo_vendedor = [codigo[0] for codigo in dados]
        nome_vendedor = []

        for item in dados:
            nome = list(item[1])
            nome = nome[0: nome.index(' ')]
            nome_vendedor.append(''.join(nome))

        return codigo_vendedor, nome_vendedor

    @property
    def dados_vendas(self):
        return self.__dados_vendas()

    @property
    def dicionario_vendas(self):
        return self.__dicionario_vendas()

    @property
    def dados_completo(self):
        return self.__dados_completo()

    def __dados_vendas(self):

        comando = 'select venda.vendedor, venda_item.venda, venda_item.produto, venda_item.qtd, ' \
                  'venda_item.desconto, venda_item.total, venda_item.qtd_devolvida, venda_item.vrcusto_composicao, ' \
                  'venda_item.descricao From venda_item INNER JOIN venda ON venda_item.venda = venda.vend_cod ' \
                  'WHERE venda_item.dtvenda BETWEEN "2022-08-05" and "2022-08-05" ORDER BY venda_item.venda;'

        self.__cursor.execute(comando)

        return self.__cursor.fetchall()

    def __dicionario_vendas(self):
        dados_gerais = dict()
        dados_vendas = dict()

        codigo_vendedor = self.__vendedores()[0]
        nome_vendedores = self.__vendedores()[1]

        for item in self.__dados_vendas():
            dados_gerais[item[1]] = []

        for item in self.__dados_vendas():
            dados_gerais[item[1]].append(item)

        for venda in dados_gerais:
            dados_vendas[venda] = {'venda': 0,
                                   'vendedor': '',
                                   'desconto': 0.0,
                                   'faturamento': 0.0,
                                   'custo': 0.0
                                   }

        for venda in self.__dados_vendas():

            qtd = float(venda[3]) - float(venda[6])
            desconto = round((float(venda[4]) / qtd) * qtd, 2)
            ponto = str(desconto).index('.')
            if len(str(desconto)[ponto:]) > 2:
                desconto = round((float(venda[4]) / qtd) * qtd)
            faturamento = round((float(venda[5]) / qtd) * qtd)
            custo = round(float(venda[7]) * qtd)

            dados_vendas[venda[1]]['venda'] = venda[1]
            dados_vendas[venda[1]]['vendedor'] = nome_vendedores[codigo_vendedor.index(venda[0])]
            dados_vendas[venda[1]]['desconto'] += desconto
            dados_vendas[venda[1]]['faturamento'] += faturamento
            dados_vendas[venda[1]]['custo'] += custo

        return dados_vendas

    def __dados_completo(self):
        despesa_fixa = DespesasRateio().despesa_fixa
        despesa_variavel = DespesasRateio().despesa_variavel

        dados_venda = self.__dicionario_vendas()

        return dados_venda


if __name__ == '__main__':
    dados = Lucratividade().dados_completo
    for info in dados.items():
        print(info)