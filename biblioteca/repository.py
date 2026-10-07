from database import conectar
from livro import Livro


class LivroRepository:

    def salvar(self, livro):
        conexao = conectar()
        cursor = conexao.cursor()

        try:
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
                    livro.quantidade_disponivel,
                ),
            )

            conexao.commit()

        finally:
            conexao.close()

    def buscar_por_isbn(self, isbn):
        conexao = conectar()
        cursor = conexao.cursor()

        try:
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
                (isbn,),
            )

            resultado = cursor.fetchone()

            if resultado is None:
                return None

            return Livro(
                isbn=resultado[0],
                titulo=resultado[1],
                autor=resultado[2],
                quantidade_disponivel=resultado[3],
            )

        finally:
            conexao.close()

    def atualizar_quantidade(self, isbn, quantidade):
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                UPDATE livros
                SET quantidade_disponivel = ?
                WHERE isbn = ?
                """,
                (quantidade, isbn),
            )

            conexao.commit()

        finally:
            conexao.close()

    def listar_todos(self):
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    isbn,
                    titulo,
                    autor,
                    quantidade_disponivel
                FROM livros
                """
            )

            resultados = cursor.fetchall()

            return [
                Livro(
                    isbn=linha[0],
                    titulo=linha[1],
                    autor=linha[2],
                    quantidade_disponivel=linha[3],
                )
                for linha in resultados
            ]

        finally:
            conexao.close()