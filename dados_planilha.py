from valores import planilhaFinal

class BuscaNaPlanilha:
    def __init__(self):
        self.__planilha = planilhaFinal()

    @property
    def planilha(self):
        return self.__planilha

    @property
    def subgrupo(self):
        return [subgrupo.strip() for subgrupo in self.planilha['SubGrupo']]

    @property
    def quantidade(self):
        return [quantidade for quantidade in self.planilha['Quantidade']]

    @property
    def custo(self):
        return [custo for custo in self.planilha['Custo']]

    @property
    def faturamento(self):
        return [faturamento for faturamento in self.planilha['Faturamento']]


if __name__ == '__main__':
    print(BuscaNaPlanilha().subgrupo)
