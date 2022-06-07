import pandas as pd
import pandas as df
from busca_planilha import BuscaPlanilhaExcel


# caminho_planilha = r"D:\Usuário\wesll\Desktop\Criação de preços\ROCHA FORTE 669636.xlsx"
caminho_planilha = BuscaPlanilhaExcel().caminho

planilha_original = pd.read_excel(caminho_planilha, sheet_name='A')

print(planilha_original)

if planilha_original.iloc[2, 0].strip() == 'Filtro:':
    planilha_editada = planilha_original.drop(index=[0, 1, 2], columns=['Unnamed: 10', 'Unnamed: 11'])
else:
    planilha_editada = planilha_original.drop(index=[0, 1], columns=['Unnamed: 10', 'Unnamed: 11'])


indices = list()

for posicao in range(0, 10):
    indices.append(planilha_editada.iat[0, posicao])


planilha_editada.columns = indices

pd = planilha_editada.drop(planilha_editada.index[[0, -1, -2]])

pd = pd.drop(['Und', 'Fração', 'Vr. Compra', 'Vr. Venda', 'Vr. Compra Novo', 'Margem', 'Vr. Venda Novo'], axis=1)
print(pd)

valores = {}
chaves = list(pd.columns)
valor = []


for coluna in range(0, pd.shape[1]):
    for linha in range(0, pd.shape[0]):
        valor.append(pd.iat[linha, coluna])
    valores[chaves[coluna]] = list(valor)
    valor.clear()


novo_df = df.DataFrame(valores)
print(novo_df)

# for dados in valores.keys():
#     print(f'{dados}: {valores[dados]}')









