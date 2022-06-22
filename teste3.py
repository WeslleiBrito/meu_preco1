from conexao_banco import conecta_banco

banco = conecta_banco()
cursor = banco.cursor()
subgrupo = dict()
cr = cursor.execute('SELECT prod_cod, prod_dsubgrupo FROM produto')

for item in cursor.fetchall():
    if item[1] in subgrupo.keys():
        subgrupo[item[1]].append(item[0])
    else:
        subgrupo[item[1]] = [item[0]]

print(subgrupo)

