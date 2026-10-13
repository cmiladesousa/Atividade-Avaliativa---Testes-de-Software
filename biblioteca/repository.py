from .database import conectar
from .livro import Livro


class LivroRepository:

    def __init__(self, conexao=None):
        self.conexao = conexao

    def salvar(self, livro):
        fechar_conexao = False
        conexao = self.conexao

        if conexao is None:
            conexao = conectar()
            fechar_conexao = True

        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO livros (
                isbn,
                titulo,
                autor,
                quantidade_disponivel
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                livro.isbn,
                livro.titulo,
                livro.autor,
                livro.quantidade_disponivel
            )
        )

        conexao.commit()

        if fechar_conexao:
            conexao.close()

    def buscar_por_isbn(self, isbn):
        fechar_conexao = False
        conexao = self.conexao

        if conexao is None:
            conexao = conectar()
            fechar_conexao = True

        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                isbn,
                titulo,
                autor,
                quantidade_disponivel
            FROM livros
            WHERE isbn = ?
            """,
            (isbn,)
        )

        resultado = cursor.fetchone()

        if fechar_conexao:
            conexao.close()

        if resultado is None:
            return None

        return Livro(
            isbn=resultado[0],
            titulo=resultado[1],
            autor=resultado[2],
            quantidade_disponivel=resultado[3]
        )

    def atualizar_quantidade(self, isbn, quantidade):
        fechar_conexao = False
        conexao = self.conexao

        if conexao is None:
            conexao = conectar()
            fechar_conexao = True

        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE livros
            SET quantidade_disponivel = ?
            WHERE isbn = ?
            """,
            (quantidade, isbn)
        )

        conexao.commit()

        if fechar_conexao:
            conexao.close()