import datetime as dt
from valores_padroes import data_inicial_padrao
from workadays import workdays


def feriados(country, state, data_inicial, data_final):
    dias = 0
    for date in workdays.get_holidays(country=country, state=state, years=range(data_inicial, data_final)):
        dias += 1

    return dias


if __name__ == '__main__':
    print(feriados(country='BR', state='BA', data_inicial=data_inicial_padrao().year,
                   data_final=dt.datetime.today().year + 1))
