import mysql.connector


config = {'host': '192.168.15.13',
          'database': 'clarionerp',
          'user': 'burite',
          'password': 'burite123',
          'port': '3307'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

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

print(dados[-1])

conn.close()
