from shutil import copyfile
from datetime import datetime


data = str(datetime.now()).replace('.', '-').replace(':', '-')

def backup():
    copyfile('base_preco.db', f'backup_banco/base_preco_{data}.db')
