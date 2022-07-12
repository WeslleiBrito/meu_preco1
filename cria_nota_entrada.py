# coding: UTF-8
import pandas as pd


class CriaNotaEntrada:

    def __init__(self, numero_nota=0, comissao=1):
        from dados_sistema import DadosSistema
        from dados_fornecedor import DadosFornecedor
        from representa_despesa import DespesaSubgrupo

        self.__dados_sistema = DadosSistema(numero_nota=numero_nota).dados_sistema
        self.__dados_fornecedor = DadosFornecedor(numero_nota=numero_nota).nota

        if comissao > 0:
            self.__comissao = comissao / 100
        else:
            self.__comissao = 0.01

        self.__despesa_variavel = DespesaSubgrupo().despesa_variavel

    @property
    def nota_entrada(self):
        return self.__calcula_preco_venda()

    def __unifica_dados(self):
        return dict(self.__dados_fornecedor, **self.__dados_sistema)

    def __calcula_preco_venda(self):

        if type(self.__dados_fornecedor) is dict and type(self.__dados_sistema) is dict:
            calulos_venda = {'despesa_variavel': [], 'valor_desconto': [], 'comissao': [], 'valor_lucro': [], 'venda': []}
            dados_unificados = self.__unifica_dados()

            for indice in range(len(self.__unifica_dados()['codigo'])):
                custo = dados_unificados['custo'][indice]
                despesa_fixa = dados_unificados['despesa_fixa'][indice]
                lucro = dados_unificados['lucro'][indice]
                desconto = dados_unificados['desconto'][indice]

                valor_monetario = custo + despesa_fixa
                valor_percentual = 1 - (self.__comissao + self.__despesa_variavel + desconto + lucro)
                preco_venda = round(valor_monetario / valor_percentual, 1)

                calulos_venda['despesa_variavel'].append(round(preco_venda * self.__despesa_variavel, 2))
                calulos_venda['valor_desconto'].append(round(preco_venda * desconto, 2))
                calulos_venda['comissao'].append(round(preco_venda * self.__comissao, 2))
                calulos_venda['valor_lucro'].append(round(preco_venda * lucro, 2))
                calulos_venda['venda'].append(preco_venda)

            return pd.DataFrame(dict(dados_unificados, **calulos_venda))

        return 'Nota não localizada ou finalizada'


if __name__ == '__main__':
    nota_entrada = CriaNotaEntrada().nota_entrada
    print(nota_entrada)

