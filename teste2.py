from conecta_banco import BancoDeDados
from conecta_banco_backup import ConectaBanco


class BackupFaturamento:
    def __init__(self):
        self.__base_indice = BancoDeDados().seleciona_coluna(coluna='indice', tabela='base_despesa_fixa')
        self.__backup_indice = ConectaBanco().seleciona_coluna(coluna='indice', tabela='base_despesa_fixa')
        self.__backup_banco = ConectaBanco().banco

    @property
    def base_indice(self):
        return [indice[0] for indice in self.__base_indice]

    @property
    def backup_indice(self):
        return [indice[0] for indice in self.__backup_indice]

    @property
    def cursor(self):
        return self.__backup_banco.cursor()

    def __insere_indice_faltante(self):
        self.cursor.execute('INSERT INTO base_despesa_fixa (descricao, grupo, quantidade, faturamento, custo, dps_total_subgrupo, dps_unit_subgrupo) VALUES (?, ?, ?, ?, ?, ?, ?)',("sub_grupo", "grupo", 0.0, 0.0, 0.0, 0.0, 0.0))

        self.__backup_banco.commit()

    def backup(self):
        tamanho_dos_bancos = len(self.base_indice) - len(self.backup_indice)

        for y in range(tamanho_dos_bancos):
            self.__insere_indice_faltante()
            print(y)


if __name__ == '__main__':
    x = BackupFaturamento()
    x.backup()

