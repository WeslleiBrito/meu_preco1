# coding: UTF-8

from datetime import date
from conexao_banco import conecta_banco
from rateio_despesa import DespesasRateio
from validador import valida_data
from valores_padroes import data_inicial_padrao


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

    @property
    def lucratividade_por_venda(self):
        return self.__lucratividade_por_venda()

    @property
    def lucratividade_por_vendedor(self):
        return self.__lucratividade_por_vendedor()

    @property
    def lucratividade_por_vendedor_resumo(self):
        return self.__lucratividade_por_vendedor_resumo()

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

    def __dados_vendas(self):

        comando = f'select venda.vendedor, venda_item.venda, venda_item.produto, venda_item.qtd, ' \
                  f'venda_item.desconto, venda_item.total, venda_item.qtd_devolvida, venda_item.vrcusto_composicao, ' \
                  f'venda_item.descricao From venda_item INNER JOIN venda ON venda_item.venda = venda.vend_cod ' \
                  f'WHERE venda_item.dtvenda BETWEEN "{self.__data_inicial}" and "{self.__data_final}" ORDER BY venda_item.venda;'

        self.__cursor.execute(comando)
        tabela_vendas_produto = self.__cursor.fetchall()
        lista_produtos = []
        for item in tabela_vendas_produto:
            if len(item) > 4 and (float(item[3]) - item[6]) > 0:
                lista_produtos.append((item[0], item[1], item[2], float(item[3]) - item[6], float(item[4]),
                                       float(item[5]), item[6], (float(item[3]) - item[6]) * item[7], item[8]))
        return lista_produtos

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
        vendedores = self.__vendedores()

        for chave in self.__numeros_venda():
            dados_venda_agrupado[chave] = {'vendedor': '', 'faturamento': 0.0, 'custo': 0.0, 'despesa fixa': 0.0,
                                           'despesa variavel': 0.0, 'comissao': 0.0, 'custo total': 0.0,
                                           'lucro': 0.0, 'porcentagem': 0.0}

        for produto in dados_venda_produto:
            faturamento = produto[5]
            custo = produto[7]
            quantidade = produto[3]
            subgrupo = produto_subgrupo[produto[2]]
            valor_fixa = despesa_fixa[subgrupo]
            fixa = valor_fixa * quantidade
            variavel = faturamento * despesa_variavel
            comissao = faturamento * self.__comissao

            custo_total = custo + fixa + variavel + comissao

            if custo_total > faturamento:
                custo_total -= comissao
                comissao = 0.0

            lucro = faturamento - custo_total
            vendedor = vendedores[1][vendedores[0].index(produto[0])]
            dados_venda_agrupado[produto[1]]['vendedor'] = vendedor
            dados_venda_agrupado[produto[1]]['faturamento'] += faturamento
            dados_venda_agrupado[produto[1]]['custo'] += custo
            dados_venda_agrupado[produto[1]]['despesa fixa'] += fixa
            dados_venda_agrupado[produto[1]]['despesa variavel'] += variavel
            dados_venda_agrupado[produto[1]]['comissao'] += comissao
            dados_venda_agrupado[produto[1]]['custo total'] += custo_total
            dados_venda_agrupado[produto[1]]['lucro'] += lucro
            dados_venda_agrupado[produto[1]]['porcentagem'] = round(dados_venda_agrupado[produto[1]]['lucro'] /
                                                                    dados_venda_agrupado[produto[1]][
                                                                        'faturamento'] * 100, 2)

        for venda in dados_venda_agrupado:
            chaves = ['faturamento', 'custo', 'despesa fixa', 'despesa variavel', 'comissao', 'custo total', 'lucro',
                      'porcentagem']

            for chave in chaves:
                dados_venda_agrupado[venda][chave] = round(dados_venda_agrupado[venda][chave], 2)

        dados_venda = dict()
        for chave in self.__numeros_venda():
            if chave in dados_venda_agrupado:
                if dados_venda_agrupado[chave]['despesa variavel']:
                    dados_venda[chave] = dados_venda_agrupado[chave]

        return dados_venda_agrupado

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
            resumo[nome] = {'quantidade vendas': 0, 'faturamento': 0.0, 'custo': 0.0, 'despesa fixa': 0.0,
                            'despesa variavel': 0.0, 'comissao': 0.0, 'custo total': 0.0, 'negativo': 0.0, 'lucro': 0.0,
                            'porcentagem': 0.0}

        for venda in vendas:
            faturamento = vendas[venda]['faturamento']
            custo = vendas[venda]['custo']
            despesa_fixa = vendas[venda]['despesa fixa']
            despesa_variavel = vendas[venda]['despesa variavel']
            comissao = vendas[venda]['comissao']
            custo_total = vendas[venda]['custo total']
            lucro = vendas[venda]['lucro']

            if lucro < 0:
                negativo = lucro
            else:
                negativo = 0.0

            resumo[vendas[venda]['vendedor']]['faturamento'] += round(faturamento, 2)
            resumo[vendas[venda]['vendedor']]['custo'] += round(custo, 2)
            resumo[vendas[venda]['vendedor']]['despesa fixa'] += round(despesa_fixa, 2)
            resumo[vendas[venda]['vendedor']]['despesa variavel'] += round(despesa_variavel, 2)
            resumo[vendas[venda]['vendedor']]['comissao'] += round(comissao, 2)
            resumo[vendas[venda]['vendedor']]['custo total'] += round(custo_total)
            resumo[vendas[venda]['vendedor']]['lucro'] += round(lucro)
            resumo[vendas[venda]['vendedor']]['negativo'] += round(negativo)

        numero_de_vendas = self.__numero_de_vendas_vendedor()

        for nome_vendedor in numero_de_vendas:

            if nome_vendedor in resumo:
                resumo[nome_vendedor]['porcentagem'] = round(resumo[nome_vendedor]['lucro'] / resumo[nome_vendedor]['faturamento'], 2) * 100

            if numero_de_vendas[nome_vendedor]:
                resumo[nome_vendedor]['quantidade vendas'] = numero_de_vendas[nome_vendedor]

        for venda in resumo:
            chaves = ['faturamento', 'custo', 'despesa fixa', 'despesa variavel', 'comissao', 'custo total', 'lucro',
                      'porcentagem']

            for chave in chaves:
                resumo[venda][chave] = round(resumo[venda][chave], 2)

        return resumo

    def __numero_de_vendas_vendedor(self):
        vendas = self.__lucratividade_por_vendedor()
        vendedores = self.__vendedores()[1]
        qtd_venda = {nome: 0 for nome in vendedores}

        for venda in vendas.items():
            qtd_venda[venda[1]['vendedor']] += 1

        return qtd_venda


if __name__ == '__main__':
    lucro_dados = Lucratividade(comissao=1).lucratividade_por_vendedor_resumo

    for info in lucro_dados.items():
        print(info)
