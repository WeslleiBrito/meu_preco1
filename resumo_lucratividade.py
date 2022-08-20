# coding: UTF-8
class ResumoLucratividade:

    def __init__(self, comissao=1):
        from lucratividade import Lucratividade

        self.__dicionario = Lucratividade(comissao=comissao).lucratividade_por_venda

    @property
    def dicionario_lista(self):
        return self.__dicionario_lista()

    @property
    def resumo(self):
        return self.__resumo()

    def __dicionario_lista(self):

        custo = []
        despesa_fixa = []
        despesa_variavel = []
        comissao = []
        custo_total = []
        faturamento = []
        lucro = []

        for valores in self.__dicionario.values():
            custo.append(valores['custo'])
            despesa_fixa.append(valores['despesa fixa'])
            despesa_variavel.append(valores['despesa variavel'])
            comissao.append(valores['comissao'])
            custo_total.append(valores['custo total'])
            faturamento.append(valores['faturamento'])
            lucro.append(valores['lucro'])

        return {'Custo': custo, 'D. Fixa': despesa_fixa, 'D. Variável': despesa_variavel, 'Comissão': comissao,
                'Total': custo_total, 'Faturamento': faturamento, 'Lucro R$': lucro}

    def __resumo(self):
        valores = {}
        chaves = ['Faturamento', 'Custo', 'D. Fixa', 'D. Variável', 'Comissão', 'Total', 'Lucro R$', 'Lucro %']

        for chave in chaves:
            if chave != 'Lucro %':
                valores[chave] = round(sum(self.__dicionario_lista()[chave]), 2)
            else:
                valores[chave] = round((valores['Lucro R$'] / valores['Faturamento']) * 100, 2)

        return valores


if __name__ == '__main__':
    resumo = ResumoLucratividade().resumo
    print(resumo)
