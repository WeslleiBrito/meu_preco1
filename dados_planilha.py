from valores import planilhaFinal

class buscaNaPlanilha:
    def __init__(self):
        self.__planilha = planilhaFinal()

    @property
    def planilha(self):
        return self.__planilha

    @property
    def subgrupo(self):
        return self.planilha['SubGrupo']

    @property
    def quantidade(self):
        return self.planilha['Quantidade']

    @property
    def custo(self):
        return self.planilha['Custo']

    @property
    def faturamento(self):
        return self.planilha['Faturamento']


if __name__ == '__main__':
    print(buscaNaPlanilha().subgrupo)
