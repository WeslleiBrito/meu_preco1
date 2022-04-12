import pandas as pd
import sqlite3 as sql

conn = sql.connect(r"D:\Usuário\wesll\Desktop\base_precos.db")
cursor = conn.cursor()

caminho = r"D:\Usuário\wesll\Desktop\Arquivos de migração\BaseSubGrupo.xlsx"

tabela = pd.read_excel(caminho, sheet_name='BaseSubGrupo')
df = tabela.drop(['Codigo'], axis=1)
df.fillna(0, inplace=True)

for linha in range(len(df)):
    sub_grupo = str(df.iloc[linha, 0]).strip()
    grupo = str(df.iloc[linha, 1]).strip()
    quantidade = df.iloc[linha, 2]

    faturamento = df.iloc[linha, 3]

    custo = df.iloc[linha, 4]
    despesa_fixa = df.iloc[linha, 5]
    fixa_unitaria = df.iloc[linha, 6]

    cursor.execute("INSERT INTO sub_grupos (sub_grupo, grupo, quantidade, faturamento, custo, despesa_fixa," \
                   " fixa_unitaria) " \
                   "VALUES (?, ?, ?, ?, ?, ?, ?)", \
                   (sub_grupo, grupo, quantidade, faturamento, custo, despesa_fixa, fixa_unitaria))

    print(f'SubGrupo: {sub_grupo} | [{linha + 1}/{len(df)}]')

conn.commit()
cursor.close()
conn.close()
