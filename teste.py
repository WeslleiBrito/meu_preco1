import pandas as pd
from conecta_banco import BancoDeDados

cursor = BancoDeDados().cursor

Codigo = [indice[0] for indice in cursor.execute('SELECT indice from base_despesa_fixa').fetchall()]
SubGrupo = [des[0] for des in cursor.execute('SELECT descricao from base_despesa_fixa').fetchall()]
Grupo = [grup[0] for grup in cursor.execute('SELECT grupo from base_despesa_fixa').fetchall()]
Quantidade = [qtd[0] for qtd in cursor.execute('SELECT quantidade from base_despesa_fixa').fetchall()]
Faturamento = [fat[0] for fat in cursor.execute('SELECT faturamento from base_despesa_fixa').fetchall()]
Custo = [cst[0] for cst in cursor.execute('SELECT custo from base_despesa_fixa').fetchall()]
DespesaFixa = [cst[0] for cst in cursor.execute('SELECT dps_total_subgrupo from base_despesa_fixa').fetchall()]
Fixa_Unitaria = [cst[0] for cst in cursor.execute('SELECT dps_unit_subgrupo from base_despesa_fixa').fetchall()]

valores = [Codigo, SubGrupo, Grupo, Quantidade, Faturamento, Custo, DespesaFixa, Fixa_Unitaria]
colunas = ['Codigo', 'SubGrupo', 'Grupo', 'Quantidade', 'Faturamento', 'Custo', 'DespesaFixa', 'Fixa Unitaria']

df = pd.DataFrame(list(zip(Codigo, SubGrupo, Grupo, Quantidade, Faturamento, Custo, DespesaFixa, Fixa_Unitaria)), columns=colunas)

df.to_excel('Exportacao\BaseSubGrupo.xlsx', sheet_name='BaseSubGrupo', index=False)
