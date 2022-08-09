# coding: UTF-8

class DataFrameLucratividade:

    def __init__(self):
        from lucratividade import Lucratividade
        self.__dados = Lucratividade(comissao=1).dados_vendas

    @property
    def dados_bruto(self):
        return self.__dados

    @property
    def dicionario(self):
        return self.__dicionario()

    def __dicionario(self):
        import pandas as pd

        dados = {'Venda': [], 'Vendedor': [], 'Quantidade': [], 'Descrição': [], 'Custo Unitário': [], 'Desconto': [],
                 'Faturamento': [], 'Comissão': [], 'Despesa Variavel': [], 'Despesa Fixa': [], 'Custo Total': [],
                 'Lucro R$': [], 'Lucro %': []}

        for item in self.__dados:
            dados['Venda'].append(item['venda'])
            dados['Vendedor'].append(item['vendedor'])
            dados['Quantidade'].append(item['quantidade'])
            dados['Descrição'].append(item['descricao'])
            dados['Custo Unitário'].append(item['custo'])
            dados['Desconto'].append(item['desconto'])
            dados['Faturamento'].append(item['faturamento'])
            dados['Comissão'].append(item['comissao'])
            dados['Despesa Variavel'].append(item['despesa_variavel'])
            dados['Despesa Fixa'].append(item['despesa_fixa'])
            dados['Custo Total'].append(item['custo_total'])
            dados['Lucro R$'].append(item['lucro'])
            dados['Lucro %'].append(item['porcentagem_lucro'])

        return pd.DataFrame(dados)


class LucroVenda:
    def __init__(self, n_venda=[]):
        from lucratividade import Lucratividade
        self.__dados = Lucratividade().dados_vendas

        if not n_venda:
            numeros = []

            for item in self.__dados:
                if item['venda'] not in numeros:
                    numeros.append(item['venda'])

            self.__n_venda = numeros
        else:
            self.__n_venda = n_venda

    @property
    def vendas(self):
        return self.__dicionario()

    @property
    def dados_bruto(self):
        return self.__dados

    def __dicionario(self):
        vendas = dict()

        for n_venda in self.__n_venda:
            vendas[n_venda] = {'Vendedor': '', 'Faturamento': 0.0, 'Custo': 0.0, 'Despesa Fixa': 0.0,
                               'Despesa Variavel': 0.0, 'Lucro': 0.0, 'Itens': 0}
        total = 0.0
        for numero in vendas:
            for venda in self.__dados:
                if venda['venda'] == numero:
                    vendas[venda['venda']]['Vendedor'] = venda['vendedor']
                    vendas[venda['venda']]['Faturamento'] += venda['faturamento']
                    vendas[venda['venda']]['Custo'] += venda['custo']
                    vendas[venda['venda']]['Despesa Fixa'] += venda['despesa_fixa']
                    vendas[venda['venda']]['Despesa Variavel'] += venda['despesa_variavel']
                    vendas[venda['venda']]['Lucro'] += venda['lucro']
                    vendas[venda['venda']]['Porcentagem'] = round(
                        vendas[venda['venda']]['Lucro'] / vendas[venda['venda']]['Faturamento'], 2) * 100
                    vendas[venda['venda']]['Itens'] += 1
                    total += venda['faturamento']
                    print(venda['descricao'])
                    print(vendas[numero])
            print(f'Total da venda: {numero} foi {total}')
            print('=' * 200)
            total = 0.0
        return vendas


if __name__ == '__main__':
    dados = LucroVenda().vendas
    for item in dados.items():
        print(item)
