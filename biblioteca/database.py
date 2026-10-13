import sqlite3

DATABASE_NAME = "biblioteca.db"


def conectar():
    return sqlite3.connect(DATABASE_NAME)


def inicializar_banco(conexao=None):
    fechar_conexao = False

    if conexao is None:
        conexao = conectar()
        fechar_conexao = True

    cursor = conexao.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS livros (
            isbn TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            quantidade_disponivel INTEGER NOT NULL
        )
        """
    )

    conexao.commit()

    if fechar_conexao:
        conexao.close()