from conecta_banco import BancoDeDados


def calcula_despesa():
    fixa = 0.00
    variavel = 0.0

    banco = BancoDeDados().banco
    cursor = banco.cursor()

    tipo_despesa = [tipo[0] for tipo in cursor.execute('SELECT tipo_despesa FROM despesas_totais').fetchall()]
    valor_despesa = [despesa[0] for despesa in cursor.execute('SELECT valor FROM despesas_totais').fetchall()]

    for posicao, tipo in enumerate(tipo_despesa):
        if tipo == 'Fixa':
            fixa += valor_despesa[posicao]
        else:
            variavel += valor_despesa[posicao]

    return [round(fixa), round(variavel)]


if __name__ == '__main__':
    print(calcula_despesa())
