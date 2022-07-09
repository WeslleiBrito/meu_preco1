from conexao_banco import conecta_banco
import datetime


class NotaEntrada:
    def __init__(self, numero_nota=0):
        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()
        self.__numero_nota = numero_nota

    @property
    def nota(self):
        return self.__dados_fornecedor()

    def __notas_abertas(self):
        self.__cursor.execute("""select 
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
WHERE N.`status` = 'F' and F.situacao = "0"
order by F.codigo, I.nitem
""")

        return self.__cursor.fetchall()

    def __dados_fornecedor(self):
        # armazenando todas as notas em aberto
        notas = self.__notas_abertas()

        # pegando todos numeros das notas colocando em um set em seguida salvando dentro da lista já convertida para inteiro
        numeros_notas = [(int(num[0]), num[1]) for num in set([(numero[0], numero[2]) for numero in notas])]

        # pegando todas as data colocando em um set em seguida salvando dentro da lista
        datas = [data for data in set(dt[2] for dt in notas)]

        # transformando as datas do tipo string em datas do tipo data
        if datas:
            for posicao, item in enumerate(datas):
                ano = int(item[6:])
                mes = int(item[3:5])
                dia = int(item[0:2])
                datas[posicao] = datetime.date(ano, mes, dia)

        # pegando a ultima data e convertendo ela para string
        ultima_data = str(max(datas))

        # editando o formato da última data para fazer comparações com as datas das notas
        data_formatada = f'{ultima_data[8:]}/{ultima_data[5:7]}/{ultima_data[0:4]}'

        # variavel de verificação de extistencia da nota no sistema, por padrão false
        testa_numero_nota = False

        # inicializando variavel
        num_nota = 0

        # inicializando dicionário da nota
        nota = {'codigo': [], 'quantidade': [], 'descricao': [], 'custo': []}

        # Avaliando a existencia do número informado, casa não informado vai ser usado o número da última nota
        if self.__numero_nota:
            for numeros in numeros_notas:
                if self.__numero_nota in numeros:
                    testa_numero_nota = True

            if testa_numero_nota:
                num_nota = self.__numero_nota
            else:
                print('Número da nota não encontrada')
        else:
            for valor in numeros_notas:
                if valor[1] == data_formatada:
                    num_nota = valor[0]

        if num_nota:
            for item in notas:
                if int(item[0]) == num_nota:
                    nota['codigo'].append(item[4])
                    nota['quantidade'].append(float(item[15]) * float(item[18]))
                    nota['descricao'].append(item[5])
                    nota['custo'].append(float(item[19]))

        return nota


if __name__ == '__main__':
    nfc = NotaEntrada(250920).nota
    print(nfc)
