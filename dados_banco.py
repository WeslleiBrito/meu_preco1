from conecta_banco import bancoDeDados


class BuscaDados:
    def __init__(self):
        self.banco = bancoDeDados()

    @property
    def busca(self):
        return self.__busca()

    @property
    def subgrupos(self):
        return [subgrupo[1] for subgrupo in self.__busca()]

    @property
    def quantidade(self):
        return [custo[2] for custo in self.__busca()]

    @property
    def custo(self):
        return [custo[3] for custo in self.__busca()]

    @property
    def faturamento(self):
        return [faturamento[4] for faturamento in self.__busca()]

    @property
    def despesa_total_fixa(self):
        return [total_despesa[5] for total_despesa in self.__busca()]

    @property
    def indices(self):
        return [indice[0] for indice in self.__busca()]

    def __busca(self):

        dados_do_banco = []

        base_subgrupo = [sub[0] for sub in self.banco.seleciona_coluna('base_despesa_fixa', 'descricao')]
        base_quantidade = [qtd[0] for qtd in self.banco.seleciona_coluna('base_despesa_fixa', 'quantidade')]
        base_custo = [cst[0] for cst in self.banco.seleciona_coluna('base_despesa_fixa', 'custo')]
        base_faturamento = [fat[0] for fat in self.banco.seleciona_coluna('base_despesa_fixa', 'faturamento')]
        base_despesa_total = [dps_total[0] for dps_total in
                              self.banco.seleciona_coluna('base_despesa_fixa', 'dps_total_subgrupo')]
        base_indices = [ind[0] for ind in self.banco.seleciona_coluna('base_despesa_fixa', 'indice')]

        for sub_grupo in base_subgrupo:

            posicao = base_subgrupo.index(sub_grupo)
            tupla_de_valores = (base_indices[posicao], sub_grupo, base_quantidade[posicao], base_custo[posicao],
                                base_faturamento[posicao], base_despesa_total[posicao])
            dados_do_banco.append(tupla_de_valores)

        return dados_do_banco


if __name__ == '__main__':
    busca = BuscaDados()

    print(len(busca.subgrupos), busca.subgrupos)
    print(len(busca.indices), busca.indices)
    print(len(busca.quantidade), busca.quantidade)
    print(len(busca.custo), busca.custo)
    print(len(busca.faturamento), busca.faturamento)
    print(len(busca.despesa_total_fixa), busca.despesa_total_fixa)
