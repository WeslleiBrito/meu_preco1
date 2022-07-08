import pandas as pd
from conecta_banco import BancoDeDados
from backup_banco import ExecutaBackup

banco = BancoDeDados().banco
cursor = banco.cursor_sqlite()

caminho = "BaseSubGrupo.xlsx"


tabela = pd.read_excel(caminho, sheet_name='BaseSubGrupo')
df = tabela.drop(['Codigo'], axis=1)
df.fillna(0, inplace=True)

ExecutaBackup().backup()

for linha in range(len(df)):
    sub_grupo = str(df.iloc[linha, 0]).strip()
    grupo = str(df.iloc[linha, 1]).strip()
    quantidade = df.iloc[linha, 2]

    faturamento = df.iloc[linha, 3]

    custo = df.iloc[linha, 4]
    despesa_fixa = df.iloc[linha, 5]
    fixa_unitaria = df.iloc[linha, 6]

    cursor.execute("INSERT INTO base_despesa_fixa (descricao, grupo, quantidade, faturamento, custo, dps_total_subgrupo," \
                   " dps_unit_subgrupo) " \
                   "VALUES (?, ?, ?, ?, ?, ?, ?)", \
                   (sub_grupo, grupo, quantidade, faturamento, custo, despesa_fixa, fixa_unitaria))

    print(f'SubGrupo: {sub_grupo} | [{linha + 1}/{len(df)}]')

banco.commit()
cursor.close()
banco.close()
