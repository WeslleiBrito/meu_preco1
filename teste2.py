import mysql.connector
from rateio_despesa_fixa import DespesasRateio
from faturamento_subgrupos import FaturamentoSubgrupos


config = {'host': '192.168.15.13',
          'database': 'clarionerp',
          'user': 'burite',
          'password': 'burite123',
          'port': '3307'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor_sqlite()

cursor.execute("""select 
N.numero Num_NF, 
N.emi_razao Fornecedor,
DATE_FORMAT(N.dtentrada,'%d%/%m%/%Y') Data,
I.nitem Item,
P.prod_cod Codigo,
P.prod_descricao,
I.und UN,
I.qtdestoque Qtd_Estoque,
I.vrcompra Vr_compra,
I.pcustos Perc_custo,
I.vrcompra Vr_Custo,
I.margem Margem,
I.vrvenda Vr_Venda,
I.pdescmax Desconto_max,
I.vrcusto_medio,
I.qtdentrada,
I.vrcompra_novo,
I.vrcustoagregado,
I.fracao,
I.custo vr_Compra_fracionado,
I.pcusto_nota Perc_custo_NF,
I.vrvenda_novo
from formacao_preco F
inner join formacao_itens I on F.codigo = I.formacao
inner join produto P on P.prod_cod = I.produto
INNER JOIN nfc N ON n.nfc_codigo = F.nf_codigo
WHERE N.`status` = 'F' and F.situacao = '0'
order by F.codigo, I.nitem""")

dados = cursor.fetchall()
subgrupos = []
cursor.execute('SELECT prod_cod, prod_dsubgrupo FROM produto')
tabela_produto = cursor.fetchall()
codigo = [cd[0] for cd in tabela_produto]
subgrupo = [sub[1] for sub in tabela_produto]

numero_nota = set([numero[0] for numero in dados])
numero_nota = [num for num in numero_nota]

nota_compra = dict()

despesas_variaveis = ['FATURAMENTO', 'CMV', 'RH(CMV)', 'RH(CV)', 'TRANSPORTE(CV)', 'TRANSPORTES (CMV)']
despesas_fixa = DespesasRateio(despesas_variaveis).total_despesa_sub_grupo
despesa_variavel = DespesasRateio(despesas_variaveis).despesa_variavel
faturamento_sub = FaturamentoSubgrupos().faturamento_por_subgrupo


for item in dados:

    if item[0] == numero_nota[-1]:
        fixa = despesas_fixa[subgrupo[codigo.index(item[4])]]
        desconto_subgrupo = faturamento_sub[subgrupo[codigo.index(item[4])]][3]

        if desconto_subgrupo < 0.15:
            desconto_subgrupo = 0.15

        nota_compra[item[5]] = [item[4], item[15], item[5], item[19], fixa, desconto_subgrupo]


print(nota_compra)


conn.close()
