import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('dados.db')

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

cursor.execute("INSERT INTO Usuarios(nome, email, senha) VALUES ('teste1', 'teste1@email', '12345');")

# Executar uma consulta SQL para obter todos os usuários
cursor.execute("SELECT * FROM Usuarios")

# Obter todos os resultados da consulta
usuarios = cursor.fetchall()

# Imprimir todos os usuários
for usuario in usuarios:
    print(usuario)

# Fechar a conexão com o banco de dados
conn.close()
