import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('dados.db')

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

# Comandos SQL para criar as tabelas
sql_usuarios = """
CREATE TABLE Usuarios (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Senha TEXT NOT NULL
);
"""

sql_livros = """
CREATE TABLE Livros (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Titulo TEXT NOT NULL,
    Autor TEXT NOT NULL,
    Ano INTEGER,
    ID_Usuario INTEGER,
    FOREIGN KEY(ID_Usuario) REFERENCES Usuarios(ID)
);
"""

sql_ofertas = """
CREATE TABLE Ofertas (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Livro_Ofertado INTEGER,
    ID_Livro_Desejado INTEGER,
    ID_Usuario_Ofertante INTEGER,
    ID_Usuario_Receptor INTEGER,
    Status TEXT CHECK(Status IN ('Aberta', 'Aceita', 'Recusada')) NOT NULL,
    FOREIGN KEY(ID_Livro_Ofertado) REFERENCES Livros(ID),
    FOREIGN KEY(ID_Livro_Desejado) REFERENCES Livros(ID),
    FOREIGN KEY(ID_Usuario_Ofertante) REFERENCES Usuarios(ID),
    FOREIGN KEY(ID_Usuario_Receptor) REFERENCES Usuarios(ID)
);
"""

# Executar os comandos SQL
cursor.execute(sql_usuarios)
cursor.execute(sql_livros)
cursor.execute(sql_ofertas)
cursor.execute("INSERT INTO Usuarios(nome, email, senha) VALUES ('teste', 'teste@email', '12345');")

# Fechar a conexão com o banco de dados
conn.close()
