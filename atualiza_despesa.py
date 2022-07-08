from busca_planilha import BuscaPlanilhaExcel
from conecta_banco import BancoDeDados
from backup_banco import ExecutaBackup
import pandas as pd
from nova_despesa_na_atualizaca import nova_despesa_durante_cadastro
from registra_geral import registra_despesa_geral
from representa_despesa import representador


class CriaDataFrameDespesa:
    def __init__(self):
        self.__caminho = BuscaPlanilhaExcel().caminho
        self.__banco = BancoDeDados().banco
        self.__cursor = self.__banco.cursor_sqlite()

    @property
    def planilha(self):
        return self.__limpeza_planilha()

    @property
    def banco(self):
        return self.__banco

    @property
    def cursor(self):
        return self.__cursor

    @property
    def atualiza(self):
        return self.__atualiza_despesas()

    def __data_frame(self):
        return pd.read_excel(self.__caminho, 'A')

    def __limpeza_planilha(self):
        planilha = self.__data_frame()
        planilha.drop(columns=['Unnamed: 5', 'Unnamed: 6'], inplace=True)
        planilha.columns = ['Despesas', 'Registros', 'Valor', 'Pago', 'A pagar']
        planilha = planilha.dropna()
        planilha = planilha.drop(planilha.index[[0, -1]])

        for despesa in planilha['Despesas']:
            if despesa == '10 - FATURAMENTO':
                indice_faturamento = planilha[planilha['Despesas'] == '10 - FATURAMENTO'].index
                planilha.drop(index=indice_faturamento, inplace=True)

        return planilha

    def __atualiza_despesas(self):
        planilha = self.planilha
        despesas_planilha = [dsp_pl for dsp_pl in planilha['Despesas']]
        valor_planilha = [valor for valor in planilha['Valor']]
        despesa_banco = [despesa[0] for despesa in
                         self.cursor.execute('SELECT descricao FROM despesas_totais').fetchall()]
        valor_banco = [valor_despesa[0] for valor_despesa in
                       self.cursor.execute('SELECT valor FROM despesas_totais').fetchall()]

        ExecutaBackup().backup()

        for indice, despesa_p in enumerate(despesas_planilha):

            if despesa_p[:2].isdigit():
                despesa_verifica = despesa_p[5:]
            else:
                despesa_verifica = despesa_p[4:]

            if despesa_verifica in despesa_banco:
                valor_total = valor_planilha[despesas_planilha.index(despesa_p)] + \
                              valor_banco[despesa_banco.index(despesa_verifica)]
                self.cursor.execute(f'UPDATE despesas_totais SET valor=? WHERE descricao=?',
                                    (valor_total, despesa_verifica))
            else:
                nova_despesa_durante_cadastro(self.cursor, despesa_verifica,
                                              valor_planilha[despesas_planilha.index(despesa_p)])

        self.banco.commit()
        registra_despesa_geral()
        representador()
        self.cursor.close()
        self.banco.close()


if __name__ == '__main__':
    pl = CriaDataFrameDespesa().atualiza
