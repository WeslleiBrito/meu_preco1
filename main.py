import pandas as pd


caminho_planilha = r"D:\Usuário\wesll\Desktop\Criação de preços\JAIME 6042022.xlsx"

planilha_original = pd.read_excel(caminho_planilha, sheet_name="A")

if planilha_original.iloc[2, 0].strip() == 'Filtro:':
    planilha_editada = planilha_original.drop(index=[0, 1, 2])
else:
    planilha_editada = planilha_original.drop(index=[0, 1])


planilha_editada = planilha_editada.drop(['Unnamed: 10', 'Unnamed: 11'], axis=1)


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


for dados in valores.keys():
    print(f'{dados}: {valores[dados]}')









