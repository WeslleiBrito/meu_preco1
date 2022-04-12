import pandas as pd
import sqlite3 as sq

caminho = r"D:\Usuário\wesll\Desktop\Arquivos de migração\Estoque.xlsx"

conn = sq.connect(r"D:\Usuário\wesll\Desktop\base_precos.db")
cursor = conn.cursor()

estoque = pd.read_excel(caminho, sheet_name='Estoque')

for linha in range(len(estoque)):
    codigo = str(estoque.iloc[linha, 0])
    descricao = str(estoque.iloc[linha, 1]).strip()
    sub_grupo = str(estoque.iloc[linha, 2]).strip()

    cursor.execute("INSERT INTO estoque (codigo, descricao, sub_grupo) VALUES (?, ?, ?)", (codigo, descricao, sub_grupo))
    print(f'Produto: {descricao} | [{linha + 1}/{len(estoque)}]')

conn.commit()
cursor.close()
conn.close()

