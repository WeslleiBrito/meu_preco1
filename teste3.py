def __dados_fornecedor(self):
    if self.__valida_numero_nota or self.__numero_nota == 0:
        # armazenando todas as notas em aberto
        notas = self.__notas_abertas()

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


        # inicializando dicionário da nota
        nota = {'codigo': [], 'quantidade': [], 'descricao': [], 'custo': []}

        if num_nota:
            for item in notas:
                if int(item[0]) == num_nota:
                    nota['codigo'].append(item[4])
                    nota['quantidade'].append(float(item[15]) * float(item[18]))
                    nota['descricao'].append(item[5])
                    nota['custo'].append(float(item[19]))

            return nota
