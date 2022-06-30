from faturamento_subgrupos import FaturamentoSubgrupos
from despesas import Despesas

faturamentos = FaturamentoSubgrupos().faturamento_subgrupo
despesas_variaveis = ['FATURAMENTO', 'CMV', 'RH(CMV)', 'RH(CV)', 'TRANSPORTE(CV)', 'TRANSPORTES (CMV)']
despesas = Despesas(despesas_variaveis).despesa_total

despesa_subgrupo = dict()

faturamento_total = sum([venda[0] for venda in faturamentos.values()])

for fatura in faturamentos:
    if faturamentos[fatura][0] > 0:
        calculo = (faturamentos[fatura][0] / faturamento_total) * despesas['Despesa Fixa'] / faturamentos[fatura][1]
        despesa_subgrupo[fatura] = round(calculo, 2)
    else:
        despesa_subgrupo[fatura] = 0.0
for desp in despesa_subgrupo.items():
    print(desp)
