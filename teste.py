import pandas as pd

caminho = r"D:\Usuário\wesll\Desktop\Criação de preços\IDB 681921.xlsx"

df = pd.read_excel(caminho, sheet_name='A')

if df.iloc[2, 0].strip() == 'Filtro:':
    df = df.drop(index=[0, 1, 2])
else:
    df = df.drop(index=[0, 1])

df = df.drop(df.index[[-1, -2]])

valores = {'Codigo': [valor for valor in df['Unnamed: 0'][1:]],
           'Descricao': [valor for valor in df['Unnamed: 1'][1:]],
           'Custo': [valor for valor in df['Relatório'][1:]]}

df = pd.DataFrame(valores)

print(df)
print(100 * '=')
print(df)
