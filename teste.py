from dados_banco import BuscaDados
from dados_planilha import BuscaNaPlanilha

banco = BuscaDados()
planilha = BuscaNaPlanilha()

encontrado = [subgrupo for subgrupo in banco.subgrupos if subgrupo in planilha.subgrupo]

