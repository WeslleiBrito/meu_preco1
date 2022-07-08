from conexao_banco import conecta_banco


class NotaEntrada:
    def __init__(self, numero_nota=0):
        self.__banco = conecta_banco()
        self.__cursor = self.__banco.cursor()
        self.__numero_nota = numero_nota

    @property
    def nota(self):
        return self.__cria_entrada_nota()

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

    def __cria_entrada_nota(self):
        # armazenando todas as notas em aberto
        notas = self.__notas_abertas()
        # pegando todos numeros das notas colocando em um set em seguida salvando dentro da lista já convertida para inteiro
        numeros_notas = [int(num) for num in set([numero[0] for numero in notas])]
        num_nota = 0
        nota = dict()

        # Avaliando a existencia do número informado, casa não informado vai ser usado o número da última nota
        if self.__numero_nota and self.__numero_nota in numeros_notas:
            num_nota = str(self.__numero_nota)
        elif self.__numero_nota and self.__numero_nota not in numeros_notas:
            print('Nota não localizada')
        else:
            num_nota = str(numeros_notas[-1])

        if num_nota:
            for item in notas:
                if item[0] == num_nota:
                    nota[item[5]] = [item[4], float(item[15]) * float(item[18]), float(item[19])]

        return nota


if __name__ == '__main__':
    nfc = NotaEntrada().nota

    print(nfc)