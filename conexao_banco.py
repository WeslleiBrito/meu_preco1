#!/usr/bin/python
# -*- coding: latin-1 -*-

import mysql.connector
import mysql.connector.errors


def conecta_banco():
    config = {'host': '192.168.15.13',
              'database': 'clarionerp',
              'user': 'burite',
              'password': 'burite123',
              'port': '3307'}
    try:
        return mysql.connector.connect(**config)
    except:
        raise Exception('Erro de comunicação com o servidor', mysql.connector.errors)


