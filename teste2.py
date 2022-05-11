import sqlite3
import io

conn = sqlite3.connect('base_preco.db')

with io.open('base_preco_backup.sql', 'w') as p:
    for linha in conn.iterdump():
        p.write('%s\n' % linha)

print('Backup salvo')
conn.close()
