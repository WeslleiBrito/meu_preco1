from conecta_banco import BancoDeDados

banco = BancoDeDados().banco
cursor = banco.cursor()


def representador():
    valores_gerais = cursor.execute('SELECT * FROM valores_gerais').fetchall()[0]
    base_despesa_fixa = cursor.execute('SELECT * FROM base_despesa_fixa').fetchall()

    dicionario = {}
    representa_fixa = valores_gerais[3] / valores_gerais[1]

    for subs in base_despesa_fixa:
        dicionario[str(subs[1])] = [subs[4], subs[3]]

    for chave in dicionario:
        faturamento = dicionario[chave][0]
        quantidade = dicionario[chave][1]

        if quantidade > 0.0:
            despesa_total = faturamento * representa_fixa
            despesa_unitaria = round(despesa_total / quantidade, 2)

            cursor.execute(f'UPDATE base_despesa_fixa SET dps_total_subgrupo=?, dps_unit_subgrupo=? WHERE descricao=?',
                           (round(despesa_total), despesa_unitaria, chave))

    banco.commit()
