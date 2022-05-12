tabela_base_despesa_fixa = """
            CREATE TABLE "base_despesa_fixa" (
        "indice"	INTEGER,
        "descricao"	TEXT,
        "grupo"	INTEGER,
        "quantidade"	REAL,
        "faturamento"	REAL,
        "custo"	REAL,
        "dps_total_subgrupo"	REAL,
        "dps_unit_subgrupo"	INTEGER,
        PRIMARY KEY("indice" AUTOINCREMENT))"""
tabela_resumo = """
                CREATE TABLE "despesa_resumo" (
                "indice"	INTEGER,
                "faturamento"	REAL,
                "custo"	REAL,
                "data_inicial"	TEXT,
                "desconto"	REAL,
                "valor_dps_fixa"	REAL,
                "valor_dps_variavel"	REAL,
                PRIMARY KEY("indice" AUTOINCREMENT))"""
tabela_estoque = """
                 CREATE TABLE "estoque" (
                "indice"	INTEGER,
                "codigo"	TEXT,
                "descricao"	TEXT,
                "sub_grupo"	TEXT,
                PRIMARY KEY("indice" AUTOINCREMENT))"""
tabela_subgrupo = """CREATE TABLE "lucro_subgrupo" (
                    "indice"	INTEGER,
                    "descricao"	TEXT,
                    "lucro"	REAL,
                    PRIMARY KEY("indice" AUTOINCREMENT))"""

tabelas = [tabela_base_despesa_fixa, tabela_resumo, tabela_estoque, tabela_subgrupo]
