
from openpyxl import load_workbook
from openpyxl.styles import Side, Border, NamedStyle, Font, Alignment

planilha = load_workbook('modelo_lucro_item.xlsx')

for linha in range(0, 100):
    planilha['Relatório'][f'A{linha + 2}'] = linha

planilha.save('testes_de_estilizacao.xlsx')
