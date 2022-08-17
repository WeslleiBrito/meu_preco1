import gspread
import pandas as pd
from resumo_mes import ResumosLucro
from teste import faturamentoDiario

CODE = '1dbh8B_BrHkI_yrBgAEj8JnK0-5q2BQxn-25Ci-sKC4U'

gc = gspread.service_account('key.json')
planilha = gc.open_by_key(CODE)

aba_dados = planilha.worksheet('Faturamentos')
faturamentos = faturamentoDiario()

for indice, chave in enumerate(faturamentos):

    aba_dados.update(f'A{indice + 1}', chave)
    aba_dados.update(f'B{indice + 1}', faturamentos[chave])

tabela = pd.DataFrame(aba_dados.get_all_records())
print(faturamentos)
