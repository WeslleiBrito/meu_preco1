import pandas as pd
from recebe_nota import RecebeNota

class LimpaNota(object):
    def __init__(self):
        self.planilha = RecebeNota().gera_dataframe()

    def limpa_nota(self):

        if self.planilha.iloc[2, 0].strip() == 'Filtro:':
            df = self.planilha.drop(index=[0, 1, 2], columns=['Unnamed: 10', 'Unnamed: 11'])
        else:
            df = self.planilha.drop(index=[0, 1], columns=['Unnamed: 10', 'Unnamed: 11'])




