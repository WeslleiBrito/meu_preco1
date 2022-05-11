from shutil import copyfile

def backup():
    copyfile('base_preco.db', 'backup_banco/base_preco_backup.db')
