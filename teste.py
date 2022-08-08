# coding: UTF-8
from datetime import date
from conexao_banco import conecta_banco
from rateio_despesa import DespesasRateio
from validador import valida_data


class Lucratividade:

    def __init__(self, data_inicial='', data_final='', comissao=0.0, venda=None, vendedor=None):

        if venda is None:
            venda = []

        if not data_inicial:
            self.__data_inicial = date.today()
        else:
            self.__data_inicial = valida_data(data_inicial)

        if not data_final:
            self.__data_final = date.today()
        else:
            self.__data_final = valida_data(data_final)

        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()
        self.__venda = venda

        if comissao == 0.0:
            self.__comissao = comissao
        else:
            self.__comissao = round(comissao / 100, 2)

        if vendedor is None:
            self.__vendedor = [nome for nome in self.__vendedores()[1]]
        else:
            self.__vendedor = vendedor

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
    def lucratividade_por_venda(self):
        return self.__lucratividade_por_venda()

    @property
    def lucratividade_por_vendedor(self):
        return self.__lucratividade_por_vendedor()

    @property
    def lucratividade_por_vendedor_resumo(self):
        return self.__lucratividade_por_vendedor_resumo()

    @property
    def vendedores(self):
        return self.__vendedores()

    def __dados_vendas(self):

        comando = f'select venda.vendedor, venda_item.venda, venda_item.produto, venda_item.qtd, ' \
                  f'venda_item.desconto, venda_item.total, venda_item.qtd_devolvida, venda_item.vrcusto_composicao, ' \
                  f'venda_item.descricao From venda_item INNER JOIN venda ON venda_item.venda = venda.vend_cod ' \
                  f'WHERE venda_item.dtvenda BETWEEN "{self.__data_inicial}" and "{self.__data_final}" ORDER BY venda_item.venda;'

        self.__cursor.execute(comando)

        return self.__cursor.fetchall()

    def __numeros_venda(self):

        if not self.__venda:
            numero = [numero[1] for numero in self.__dados_vendas()]
            return numero

        return self.__venda

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
                                   'custo': 0.0,
                                   'despesa fixa': 0.0,
                                   'despesa variavel': 0.0,
                                   'comissao': 0.0,
                                   'custo total': 0.0,
                                   'lucro': 0.0,
                                   'porcentagem': 0.0
                                   }

        for venda in self.__dados_vendas():

            qtd = float(venda[3]) - float(venda[6])
            if float(venda[4]) != 0 and qtd != 0:
                desconto = round((float(venda[4]) / qtd) * qtd, 2)
                faturamento = round((float(venda[5]) / qtd) * qtd, 2)
            else:
                desconto = 0.0
                faturamento = 0.0

            ponto = str(desconto).index('.')
            if len(str(desconto)[ponto:]) > 2:
                desconto = round((float(venda[4]) / qtd) * qtd)

            ponto = str(faturamento).index('.')
            if len(str(faturamento)[ponto:]) > 2:
                faturamento = round((float(venda[5]) / qtd) * qtd)
            custo = round(float(venda[7]) * qtd, 2)

            dados_vendas[venda[1]]['venda'] = venda[1]
            dados_vendas[venda[1]]['vendedor'] = nome_vendedores[codigo_vendedor.index(venda[0])]
            dados_vendas[venda[1]]['desconto'] += desconto
            dados_vendas[venda[1]]['faturamento'] += faturamento
            dados_vendas[venda[1]]['custo'] += custo

        return dados_vendas

    def __produto_subgrupo(self):
        comando = 'SELECT prod_cod, prod_dsubgrupo FROM produto'
        self.__cursor.execute(comando)
        return {item[0]: item[1] for item in self.__cursor.fetchall()}

    def __lucratividade_por_venda(self):
        despesa_fixa = DespesasRateio().despesa_fixa
        despesa_variavel = DespesasRateio().despesa_variavel

        produto_subgrupo = self.__produto_subgrupo()
        dados_venda_agrupado = self.__dicionario_vendas()
        dados_venda_produto = self.__dados_vendas()

        for item in self.__numeros_venda():
            fixa = 0.0

            for produto in dados_venda_produto:
                if produto[1] == item:
                    codigo = produto[2]
                    quantidade = float(produto[3])
                    fixa += despesa_fixa[produto_subgrupo[codigo]] * quantidade

            faturamento = dados_venda_agrupado[item]['faturamento']

            variavel = despesa_variavel * faturamento
            comissao = faturamento * self.__comissao
            custo_total = round(fixa + variavel + comissao + dados_venda_agrupado[item]['custo'], 2)

            if custo_total > faturamento:
                custo_total = round(custo_total - comissao)
                comissao = 0.0

            lucro = faturamento - custo_total

            dados_venda_agrupado[item]['despesa fixa'] = round(fixa, 2)
            dados_venda_agrupado[item]['despesa variavel'] = round(variavel, 2)
            dados_venda_agrupado[item]['comissao'] = round(comissao, 2)
            dados_venda_agrupado[item]['custo total'] = round(custo_total, 2)
            dados_venda_agrupado[item]['lucro'] = round(lucro, 2)
            if lucro != 0 and faturamento != 0:
                dados_venda_agrupado[item]['porcentagem'] = round((lucro / faturamento) * 100, 2)
            dados_venda_agrupado[item]['porcentagem'] = 0.0

        dados_venda = dict()
        for chave in self.__numeros_venda():
            if chave in dados_venda_agrupado:
                if dados_venda_agrupado[chave]['despesa variavel']:
                    dados_venda[chave] = dados_venda_agrupado[chave]

        return dados_venda

    def __lucratividade_por_vendedor(self):
        vendas = self.__lucratividade_por_venda()
        valores = dict()

        for vendedor in self.__vendedor:
            for venda in vendas:
                if vendas[venda]['vendedor'] == vendedor:
                    valores[venda] = vendas[venda]

        return valores

    def __lucratividade_por_vendedor_resumo(self):
        resumo = dict()
        vendas = self.__lucratividade_por_vendedor()
        vendedores = [vendedor['vendedor'] for vendedor in vendas.values()]

        for nome in vendedores:
            resumo[nome] = {'faturamento': 0.0, 'custo': 0.0, 'despesa fixa': 0.0, 'despesa variavel': 0.0,
                            'comissao': 0.0,
                            'custo total': 0.0, 'negativo': 0.0, 'lucro': 0.0, 'porcentagem': 0.0}

        for vendedor in vendedores:
            faturamento = 0.0
            custo = 0.0
            despesa_fixa = 0.0
            despesa_variavel = 0.0
            comissao = 0.0
            custo_total = 0.0
            lucro = 0.0
            negativo = 0.0

            for venda in vendas:
                if vendas[venda]['vendedor'] == vendedor:
                    faturamento += vendas[venda]['faturamento']
                    custo += vendas[venda]['custo']
                    despesa_fixa += vendas[venda]['despesa fixa']
                    despesa_variavel += vendas[venda]['despesa variavel']
                    comissao += vendas[venda]['comissao']
                    custo_total += vendas[venda]['custo total']

                    if vendas[venda]['lucro'] < 0:
                        negativo += vendas[venda]['lucro']

                    lucro += vendas[venda]['lucro']

                    resumo[vendedor]['faturamento'] = round(faturamento, 2)
                    resumo[vendedor]['custo'] = round(custo, 2)
                    resumo[vendedor]['despesa fixa'] = round(despesa_fixa, 2)
                    resumo[vendedor]['despesa variavel'] = round(despesa_variavel, 2)
                    resumo[vendedor]['comissao'] = round(comissao, 2)
                    resumo[vendedor]['custo total'] = round(custo_total, 2)
                    resumo[vendedor]['negativo'] = round(negativo, 2)
                    resumo[vendedor]['lucro'] = round(lucro, 2)
                    resumo[vendedor]['porcentagem'] = round((lucro / faturamento) * 100, 1)

        return resumo


if __name__ == '__main__':
    dados = Lucratividade(comissao=1, data_inicial='2022-08-01',
                          ).lucratividade_por_vendedor_resumo

    for info in dados.items():
        print(info)
