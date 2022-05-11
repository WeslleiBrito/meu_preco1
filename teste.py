import io
import sqlite3

conn = sqlite3.connect('base_preco.db')
with io.open('base_preco.db', 'r') as base:
    for linha in conn.iterdump():
        print(linha)
