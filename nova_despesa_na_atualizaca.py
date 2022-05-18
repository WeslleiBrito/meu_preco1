#!/usr/bin/python
# -*- coding: latin-1 -*-

def nova_despesa_durante_cadastro(cursor, descricao, valor):
    while True:
        resposta = input(f'Despesa {descricao}'
                         f' não localizada no banco, deseja inserir essa despesa? [1 - Sim, 2 - Não]: ')

        if resposta.isdigit():

            if int(resposta) == 1:

                while True:
                    tipo_despesa = input(f'Qual o tipo de despesa? [1 - Fixa, 2 - Variável]: ')

                    if tipo_despesa.isdigit():

                        if int(tipo_despesa) == 1:

                            tipo_despesa = 'Fixa'

                            cursor.execute('INSERT INTO despesas_totais (descricao, tipo_despesa, valor) VALUES (?, '
                                           '?, ?)', (descricao, tipo_despesa, valor))

                            return print(f'Despesa {descricao} inserida com sucesso! ')

                        elif int(tipo_despesa) == 2:

                            tipo_despesa = 'Variável'

                            cursor.execute(
                                'INSERT INTO despesas_totais (descricao, tipo_despesa, valor) VALUES (?, ?, ?)',
                                (descricao, tipo_despesa, valor))

                            return print(f'Despesa {descricao} inserida com sucesso! ')
                        else:
                            print('Informe um valor entre 1 e 2.')
                    else:
                        print('Informe apenas número')

            elif int(resposta) == 2:
                break
            else:
                print('Informe um valor entre 1 e 2.')
        else:
            print('Informe apenas número')
