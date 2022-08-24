# coding: UTF-8
from openpyxl import load_workbook
from openpyxl.styles import Side, Border, NamedStyle, Font, Alignment
from datetime import date
from lucratividade import Lucratividade
from resumo_lucratividade import CriaPlanilhaLucratividadeItem

dicionario_lucratividade_item = Lucratividade(comissao=1).lucratividade_por_item
planilha_base = CriaPlanilhaLucratividadeItem(dicionario_lucratividade_item).dicionario_lista

planilha_modelo = load_workbook('modelo_lucro_item.xlsx')
data_atual = str(date.today())
dia = data_atual[8:]
mes = data_atual[5:7]
ano = data_atual[0:4]

bordas = Side(border_style="thin", color="000000")
valores = []
fonte = NamedStyle(name='Calibri')
fonte.font = Font(bold=True, size='11')

colunas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
indice_valores = [0, 1, 2, 3, 4, 7, 8, 9, 10, 11]

faturamento = 0.0
custo = 0.0
comissao = 0.0
custo_despesa = 0.0
lucro = 0.0
percentual = 0.0
linha_final = 5

for index, dados in enumerate(planilha_base.values):
    linha_final += index
    custo += dados[4]
    comissao += dados[7]
    custo_despesa += dados[8]
    faturamento += dados[9]
    lucro += dados[10]

    for indice, coluna in zip(indice_valores, colunas):
        planilha_modelo['Relatório'][f'{coluna}{index + 2}'] = dados[indice]
        planilha_modelo['Relatório'][f'{coluna}{index + 2}'].style = fonte
        planilha_modelo['Relatório'][f'{coluna}{index + 2}'].alignment = Alignment(horizontal="center",
                                                                                   vertical="center")
        planilha_modelo['Relatório'][f'{coluna}{index + 2}'].border = Border(top=bordas, left=bordas, right=bordas,
                                                                             bottom=bordas)

print(linha_final)
index += 5
planilha_modelo['Relatório'][f'G{index}'] = 'Faturamento'
planilha_modelo['Relatório'][f'H{index}'] = faturamento
planilha_modelo['Relatório'][f'G{index + 1}'] = 'Custo'
planilha_modelo['Relatório'][f'H{index + 1}'] = custo
planilha_modelo['Relatório'][f'G{index + 2}'] = 'Comissão'
planilha_modelo['Relatório'][f'H{index + 2}'] = comissao
planilha_modelo['Relatório'][f'G{index + 3}'] = 'CMV+Despesa'
planilha_modelo['Relatório'][f'H{index + 3}'] = custo_despesa
planilha_modelo['Relatório'][f'G{index + 4}'] = 'Lucro R$'
planilha_modelo['Relatório'][f'H{index + 4}'] = lucro

if lucro and faturamento != 0:
    planilha_modelo['Relatório'][f'G{index + 5}'] = 'Lucro %'
    planilha_modelo['Relatório'][f'H{index + 5}'] = round(lucro / faturamento, 2) * 100

planilha_modelo.save(f'lucratividade_{dia}-{mes}-{ano}.xlsx')
