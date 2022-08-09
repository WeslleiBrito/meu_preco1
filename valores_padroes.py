def data_inicial_padrao(servidor='ServidorBalcao'):
    from conexao_banco import conecta_banco
    banco = conecta_banco(nome_host=servidor)
    cursor = banco.cursor()
    cursor.execute('SELECT rateio_dtvencimento FROM pagar_rateio')
    data = cursor.fetchall()[0][0]
    return data


if __name__ == '__main__':
    print(data_inicial_padrao())
