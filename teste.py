import pandas as pd
import pdfplumber

pdf = pdfplumber.open(r"D:\Usuário\wesll\Desktop\Criação de preços\rptListaPrecoModelo2.pdf")
p = pdf.pages[0]

tabela = p.extract_table()

print(tabela)
df = pd.DataFrame(tabela[:1], columns=tabela[0])

