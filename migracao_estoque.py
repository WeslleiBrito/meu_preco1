import pandas as pd
from conecta_banco import bancoDeDados

banco = bancoDeDados().banco
cursor = banco.cursor()

estoque = pd.read_excel("Estoque.xlsx", sheet_name='Estoque')

for linha in range(len(estoque)):
    codigo = str(estoque.iloc[linha, 0])
    descricao = str(estoque.iloc[linha, 1]).strip()
    sub_grupo = str(estoque.iloc[linha, 2]).strip()

    cursor.execute("INSERT INTO estoque (codigo, descricao, sub_grupo) VALUES (?, ?, ?)", (codigo, descricao, sub_grupo))
    print(f'Produto: {descricao} | [{linha + 1}/{len(estoque)}]')


banco.commit()
cursor.close()
banco.close()
