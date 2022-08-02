# coding: UTF-8
from datetime import date
from conexao_banco import conecta_banco
from rateio_despesa import DespesasRateio


def espaco_nomes(descricao, valor, limite=25):
    valor = len(str(valor))
    descricao = len(str(descricao))

    return limite - (valor + descricao)


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

    @property
    def vendedores(self):
        return self.__vendedores()

    def __vendedores(self):
        self.__cursor.execute('SELECT fun_cod,  fun_nome FROM funcionario;')
        dados = self.__cursor.fetchall()
        codigo_vendedor = [codigo[0] for codigo in dados]
        nome_vendedor = []

        for item in dados:
            nome = list(item[1])
            nome = nome[0: nome.index(' ')]
            nome_vendedor.append(''.join(nome))

        return codigo_vendedor, nome_vendedor

    def __dados_vendas(self):
        dados_vendas = []
        codigo_vendedor = self.__vendedores()[0]
        nome_vendedores = self.__vendedores()[1]

        comando = f'SELECT venda_item.venda, venda_item.produto, venda_item.descricao, ' \
                  f'SUM(venda_item.qtd - venda_item.qtd_devolvida) as quantidade, ' \
                  f'SUM(venda_item.vrcusto_composicao * (venda_item.qtd - venda_item.qtd_devolvida)) as custo,' \
                  f'SUM(venda_item.desconto) as desconto, SUM(venda_item.total) as faturamento,' \
                  f'SUM(venda_item.qtd_devolvida) as quantidade_devolvida, venda_item.venda, ' \
                  f'venda.vendedor FROM venda_item INNER JOIN venda ON venda_item.venda = venda.vend_cod ' \
                  f'WHERE venda.finalizacao BETWEEN "{self.__data_inicial}" AND "{self.__data_final}" ' \
                  f'GROUP BY venda_item.descricao ORDER BY venda_item.venda DESC;'

        self.__cursor.execute(comando)

        for item in self.__cursor.fetchall():
            vendedor = nome_vendedores[codigo_vendedor.index(item[9])]
            dados_vendas.append({'venda': item[0],
                                 'vendedor': vendedor,
                                 'codigo': item[1],
                                 'descricao': item[2],
                                 'quantidade': item[3],
                                 'custo': item[4],
                                 'desconto': float(item[5]),
                                 'faturamento': float(item[6]),
                                 'qtd_devolvilda': item[7],
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
            fixa = round(item['quantidade'] * despesa_fixa[subgrupo[posicao]], 2)
            variavel = round(item['faturamento'] * despesa_variavel, 2)
            comissao = round(item['faturamento'] * self.__comissao, 2)
            dados_vendas[indice]['comissao'] = comissao
            dados_vendas[indice]['despesa_variavel'] = variavel
            dados_vendas[indice]['despesa_fixa'] = fixa
            dados_vendas[indice]['custo_total'] = round(dados_vendas[indice]['custo'] + comissao + variavel + fixa, 2)

            if dados_vendas[indice]['faturamento'] - dados_vendas[indice]['custo_total'] > 0:
                dados_vendas[indice]['lucro'] = round(
                    dados_vendas[indice]['faturamento'] - dados_vendas[indice]['custo_total'], 2)
            else:
                dados_vendas[indice]['comissao'] = 0.0
                dados_vendas[indice]['custo_total'] = round(dados_vendas[indice]['custo'] + comissao + variavel + fixa,
                                                            2)
                dados_vendas[indice]['lucro'] = round(
                    dados_vendas[indice]['faturamento'] - dados_vendas[indice]['custo_total'], 2)

            dados_vendas[indice]['porcentagem_lucro'] = round(
                dados_vendas[indice]['lucro'] / dados_vendas[indice]['faturamento'], 2)

        return dados_vendas


if __name__ == '__main__':
    lucros = Lucratividade(comissao=1).dados_vendas

    custo = 0.0
    faturamento = 0.0
    despesa_vr = 0.0
    comissao = 0.0
    fixa = 0.0
    negativos = 0.0

    for item in lucros:
        custo += item['custo']
        faturamento += item['faturamento']
        despesa_vr += item['despesa_variavel']
        comissao += item['comissao']
        fixa += item['despesa_fixa']
        if item['lucro'] < 0:
            negativos += item['lucro']

        print(item)
    custo_total = round(custo + despesa_vr + comissao + fixa, 2)
    lucro = round(faturamento - custo_total, 2)

    nome = ['Faturamento', 'Custo', 'Despesa Variavel', 'Comissão', 'Despesa Fixa', 'Custo total', 'Lucro/Prejuízo',
            'Prejuízos']
    valores = [round(faturamento, 2), round(custo, 2), round(despesa_vr, 2), round(comissao, 2), round(fixa, 2),
               round(custo_total, 2), round(lucro, 2), round(negativos, 2)]

    print()
    for n, v in zip(nome, valores):
        print(f'{n} {espaco_nomes(n, v) * "-"} {v}')
