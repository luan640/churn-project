import csv
import sqlite3
import os

# Diretório onde estão localizados os arquivos CSV
pasta_csv = 'setup/'

# Lista todos os arquivos CSV na pasta
tabelas_csv = [arquivo for arquivo in os.listdir(pasta_csv) if arquivo.endswith('.csv')]

# Conectando ao banco de dados SQLite
conn = sqlite3.connect('bd_cs_go_.sqlite')
cursor = conn.cursor()

for tabela_csv in tabelas_csv:
   
    with open(pasta_csv + tabela_csv, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        colunas = next(csv_reader)

        # Nome da tabela a partir do nome do arquivo CSV
        nome_tabela = tabela_csv.replace('.csv', '')

        declaracao_colunas = ", ".join(f"{coluna} TEXT" for coluna in colunas)

        # Criando a tabela no banco de dados se ela ainda não existe
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({declaracao_colunas})")

        for linha in csv_reader:
            valores = ", ".join(["?"] * len(colunas))
            declaracao_insert = f"INSERT INTO {nome_tabela} VALUES ({valores})"
            cursor.execute(declaracao_insert, tuple(linha))

# Salvando as alterações e feche a conexão com o banco de dados
conn.commit()
conn.close()
