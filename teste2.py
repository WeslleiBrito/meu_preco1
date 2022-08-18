import gspread
import pandas as pd
from faturamento_diario import FaturamentoDiario
from datetime import date

CODE = '1dbh8B_BrHkI_yrBgAEj8JnK0-5q2BQxn-25Ci-sKC4U'

gc = gspread.service_account('key.json')
planilha = gc.open_by_key(CODE)

aba_dados = planilha.worksheet('Faturamentos')
faturamentos = FaturamentoDiario().faturamentoDiario
datas = [data for data in faturamentos.keys()]

for dias in datas:
    dia = int(dias[0:2])
    mes = int(dias[3:5])
    ano = int(dias[6:])

    if date(ano, mes, dia).weekday() == 6:
        del faturamentos[dias]

for indice, chave in enumerate(faturamentos):
    aba_dados.update(f'A{indice + 1}', chave)
    aba_dados.update(f'B{indice + 1}', faturamentos[chave])

tabela = pd.DataFrame(aba_dados.get_all_records())
print(datas)
