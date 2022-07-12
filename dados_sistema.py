class DadosSistema:
    def __init__(self, numero_nota=0):
        from dados_fornecedor import DadosFornecedor
        from conexao_banco import conecta_banco
        from representa_despesa import DespesaSubgrupo
        from lucro_subgrupo import LucroSubgrupo
        from desconto_subgrupo import DescontoPorSubgrupo
        from validador import valida_inteiro

        numero = valida_inteiro(numero_nota)

        self.__nota_fornecedor = DadosFornecedor(numero_nota=numero).nota
        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()
        self.__despesas_fixas = DespesaSubgrupo().despesa_fixa_subgrupo
        self.__lucros_subgrupos = LucroSubgrupo().lucro_por_subgrupo
        self.__descontos_subgrupos = DescontoPorSubgrupo().desconto_subgrupo

    @property
    def dados_sistema(self):
        return self.__busca_dados_sistema()

    def __busca_dados_sistema(self):
        if type(self.__nota_fornecedor) is dict:
            codigo_nota = self.__nota_fornecedor['codigo']
            despesas_fixas_lucro_desconto = {'despesa_fixa': [], 'lucro': [], 'desconto': []}
            self.__cursor.execute('SELECT prod_cod, prod_dsubgrupo FROM produto')
            dados_produtos_banco = self.__cursor.fetchall()
            codigo_banco = [cod[0] for cod in dados_produtos_banco]
            subgrupos = [subgrupo[1] for subgrupo in dados_produtos_banco]

            for codigo in codigo_nota:
                despesas_fixas_lucro_desconto['despesa_fixa'].append \
                    (self.__despesas_fixas[subgrupos[codigo_banco.index(codigo)]])
                despesas_fixas_lucro_desconto['lucro'].append \
                    (self.__lucros_subgrupos[subgrupos[codigo_banco.index(codigo)]])
                despesas_fixas_lucro_desconto['desconto'].append \
                    (self.__descontos_subgrupos[subgrupos[codigo_banco.index(codigo)]])

            return despesas_fixas_lucro_desconto

        return False


if __name__ == '__main__':
    dados = DadosSistema(numero_nota='m').dados_sistema
    print(dados)
