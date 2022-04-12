import pandas as pd
local_arquivo = r"D:\Usuário\wesll\Desktop\Criação de preços\ROCHA FORTE 669636.xlsx"

class RecebeNota:
    def __init__(self, caminho=local_arquivo, nome_da_aba='A'):
        self.caminho = caminho
        self.aba = nome_da_aba

    def gera_dataframe(self):
        df = pd.read_excel(self.caminho, sheet_name=self.aba)
        return df


if __name__ == '__main__':
    tabela = RecebeNota(r"D:\Usuário\wesll\Desktop\Criação de preços\ROCHA FORTE 669636.xlsx", 'A').gera_dataframe()
    print(tabela)
