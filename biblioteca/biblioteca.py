import sqlite3

from livro import Livro
from repository import LivroRepository
from validators import validar_livro, validar_isbn


class Biblioteca:

    def __init__(self):
        self.repository = LivroRepository()

    def cadastrar_livro(self, isbn, titulo, autor, quantidade):
        isbn, titulo, autor, quantidade = validar_livro(
            isbn,
            titulo,
            autor,
            quantidade,
        )

        if self.repository.buscar_por_isbn(isbn):
            raise ValueError(
                f"Já existe um livro cadastrado com o ISBN {isbn}."
            )

        livro = Livro(
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            quantidade_disponivel=quantidade,
        )

        try:
            self.repository.salvar(livro)

        except sqlite3.IntegrityError:
            raise ValueError(
                f"Já existe um livro cadastrado com o ISBN {isbn}."
            )

        return livro

    def consultar_livro(self, isbn):
        isbn = validar_isbn(isbn)

        livro = self.repository.buscar_por_isbn(isbn)

        if livro is None:
            raise ValueError(
                f"Livro com ISBN {isbn} não encontrado."
            )

        return livro

    def verificar_disponibilidade(self, isbn):
        livro = self.consultar_livro(isbn)

        return livro.esta_disponivel()

    def emprestar_livro(self, isbn):
        livro = self.consultar_livro(isbn)

        if not livro.esta_disponivel():
            raise ValueError(
                f"Não há exemplares disponíveis de '{livro.titulo}'."
            )

        livro.quantidade_disponivel -= 1

        self.repository.atualizar_quantidade(
            livro.isbn,
            livro.quantidade_disponivel,
        )

        return livro

    def devolver_livro(self, isbn):
        livro = self.consultar_livro(isbn)

        livro.quantidade_disponivel += 1

        self.repository.atualizar_quantidade(
            livro.isbn,
            livro.quantidade_disponivel,
        )

        return livro

    def listar_livros(self):
        return self.repository.listar_todos()