import pandas as pd
import sqlite3 as sq

caminho = r"D:\Usuário\wesll\Desktop\Arquivos de migração\mkpsub.xlsx"
banco = sq.connect(r"D:\Usuário\wesll\Desktop\base_precos.db")
cursor = banco.cursor()

tabela_lucro = pd.read_excel(caminho, sheet_name='mkpsub')

tabela_lucro = tabela_lucro.drop(['Código', 'identificação', '% Part Despesa Fixa'], axis=1)

for linha in range(len(tabela_lucro)):
    sub_grupo = tabela_lucro.iloc[linha, 0]
    lucro = tabela_lucro.iloc[linha, 1]

    cursor.execute("INSERT INTO lucro_produto (subGrupo, lucro) VALUES (?, ?)", (sub_grupo, lucro))
    print(f'SubGrupo: {sub_grupo} | [{linha}/{len(tabela_lucro)}]')

banco.commit()
cursor.close()
banco.close()