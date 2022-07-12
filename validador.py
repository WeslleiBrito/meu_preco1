# coding: UTF-8
from conexao_banco import conecta_banco


def valida_inteiro(valor):
    while True:
        try:
            valor = int(valor)
        except ValueError:
            valor = input('Informe um valor numérico válido: ')
        else:
            return int(valor)


def exite_nota(numero=0):
    banco = conecta_banco()
    cursor = banco.cursor()

    cursor.execute('SELECT nf FROM formacao_preco WHERE situacao ="0"')

    numeros = [int(num[0]) for num in cursor.fetchall()]

    if numero == 0 or numero in numeros:
        return True
    else:
        return 'Número não localizado ou nota já efetivada.'

