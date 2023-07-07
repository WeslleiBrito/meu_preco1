
def arredonda_para_cima(valor, casas_decimais=0):
	numero_inteiro = int(valor)

	if valor < 1.99:
		casas_decimais = 1


	if casas_decimais == 0:
		resto = 1 - (valor - numero_inteiro)

		return valor + resto

	else:
		if casas_decimais > 0:
			numero_str = str(float(valor))
			posicao_ponto = numero_str.find('.')
			resto = numero_str[posicao_ponto + 1: posicao_ponto + 2 + casas_decimais]

			if casas_decimais != 1:
				divisor = int(f'1{casas_decimais * "0"}')
			else:
				divisor = 100

			ultimo_digito = (10 - int(resto[-1])) / divisor
			arredondado = (int(resto) / divisor) + ultimo_digito + numero_inteiro

			if len(str(arredondado)) < len(str(valor)):

				return arredondado

			else:

				tamanho_resto = len(str(resto))
				divisor = int(f'1{tamanho_resto * "0"}')
				ultimo_digito = (10 - int(resto[-1])) / divisor

				return (int(resto) / divisor) + ultimo_digito + numero_inteiro
		
	return valor
