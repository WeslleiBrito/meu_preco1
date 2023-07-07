#!/usr/bin/python
# -*- coding: latin-1 -*-

import mysql.connector
import mysql.connector.errors
from busca_ip_servidor import busca_ip


def conecta_banco(nome_host='servidorBalcao'):

    config = {'host': f'{busca_ip(nome_host)}',
              'database': 'clarionerp',
              'user': 'burite',
              'password': 'burite123',
              'port': '3307'}
    try:
        return mysql.connector.connect(**config)
    except:
        raise Exception('Erro de comunica��o com o servidor',
                        mysql.connector.errors)
