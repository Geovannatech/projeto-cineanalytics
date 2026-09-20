import sqlite3
import pandas as pd

print("Lendo o arquivo CSV...")
df = pd.read_csv("filmes_populares.csv")

# Tratamento da data de lançamento
df["data_lancamento"] = pd.to_datetime(df["data_lancamento"], errors="coerce")

# Conecta ao banco SQLite (cria o arquivo 'cinema.db')
conn = sqlite3.connect("cinema.db")

# Grava os dados na tabela 'tb_filmes'
df.to_sql("tb_filmes", conn, if_exists="replace", index=False)

print(
    "Tabela 'tb_filmes' criada e alimentada com sucesso no arquivo"
    " 'cinema.db'!\n"
)

# Consulta SQL de teste
query_validacao = """
SELECT titulo, nota_media, orcamento, bilheteria 
FROM tb_filmes 
ORDER BY bilheteria DESC 
LIMIT 5;
"""

top_5_filmes = pd.read_sql_query(query_validacao, conn)
print("--- TOP 5 FILMES DE MAIOR BILHETERIA (Consulta SQL) ---")
print(top_5_filmes)

conn.close()