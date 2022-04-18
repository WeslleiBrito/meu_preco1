import sqlite3 as sq
localhost = r"D:\Usuário\wesll\Desktop\base_precos.db"
class ConectaBanco:
    def __init__(self):
        pass

    def conector(self):
        with sq.connect(localhost) as conn:
            return conn.cursor()
