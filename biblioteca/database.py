import sqlite3

DATABASE_NAME = "biblioteca.db"


def conectar():
    conexao = sqlite3.connect(DATABASE_NAME)

    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def inicializar_banco(conexao=None):
    fechar_conexao = False

    if conexao is None:
        conexao = conectar()
        fechar_conexao = True

    try:
        cursor = conexao.cursor()

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS livros (
                isbn TEXT PRIMARY KEY,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                quantidade_disponivel INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1)),
                multa INTEGER NOT NULL DEFAULT 0
                    CHECK (multa >= 0)
            );

            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1)),

                FOREIGN KEY (isbn) REFERENCES livros(isbn),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
            """
        )

        conexao.commit()

    finally:
        if fechar_conexao:
            conexao.close()