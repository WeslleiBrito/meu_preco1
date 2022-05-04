from conecta_banco import bancoDeDados


class BuscaDados:
    def __init__(self):
        pass

    @property
    def banco_subgrupos(self):
        return self.__busca()[0]

    @property
    def banco_quantidade(self):
        return self.__busca()[1]

    @property
    def banco_custo(self):
        return self.__busca()[2]

    @property
    def banco_faturamento(self):
        return self.__busca()[3]

    @property
    def banco_despesa_total_fixa(self):
        return self.__busca()[4]

    def __busca(self):
        banco = bancoDeDados()
        base_subgrupo = [sub[0] for sub in banco.seleciona_coluna('base_despesa_fixa', 'descricao')]
        base_quantidade = [qtd[0] for qtd in banco.seleciona_coluna('base_despesa_fixa', 'quantidade')]
        base_custo = [cst[0] for cst in banco.seleciona_coluna('base_despesa_fixa', 'custo')]
        base_faturamento = [fat[0] for fat in banco.seleciona_coluna('base_despesa_fixa', 'faturamento')]
        base_despesa_total = [dps_total[0] for dps_total in
                              banco.seleciona_coluna('base_despesa_fixa', 'dps_total_subgrupo')]

        return base_subgrupo, base_quantidade, base_custo, base_faturamento, base_despesa_total


if __name__ == '__main__':
    busca = BuscaDados()
    print(busca.banco_quantidade)
