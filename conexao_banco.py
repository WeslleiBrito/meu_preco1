#!/usr/bin/python
# -*- coding: latin-1 -*-

import mysql.connector


config = {'host': '192.168.15.13',
          'database': 'clarionerp',
          'user': 'burite',
          'password': 'burite123',
          'port': '3307'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

cursor.execute('SELECT  FROM pagar_rateio F INNER JOIN venda_item')