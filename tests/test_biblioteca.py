import pytest
from unittest.mock import patch

from biblioteca.livro import Livro
from biblioteca.biblioteca import (
    cadastrar_livro,
    empestar_livro,
    devolver_livro
)


class TestBiblioteca:
    # Foram feitos os testes de exceção, falta os testes de sucesso
    # Foi feito o isolamento dos testes com o uso do mock
    @patch("biblioteca.biblioteca.LivroRepository")
    def test_cadastrar_livro_valido(self, MockRepository):
        isbn = "978-3-16-148410-0"
        titulo = "O Senhor dos Anéis"
        autor = "J.R.R. Tolkien"
        quantidade = 5

        repository_mock = MockRepository.return_value

        repository_mock.buscar_por_isbn.return_value = None

        livro = cadastrar_livro(
            isbn,
            titulo,
            autor,
            quantidade
        )

        assert livro.isbn == isbn
        assert livro.titulo == titulo
        assert livro.autor == autor
        assert livro.quantidade_disponivel == quantidade

        repository_mock.buscar_por_isbn.assert_called_once_with(isbn)
        repository_mock.salvar.assert_called_once_with(livro)


    @patch("biblioteca.biblioteca.LivroRepository")
    def test_cadastrar_livro_invalido(self, MockRepository):
        isbn = "978-3-16-148410-0a"
        titulo = "O Senhor dos Anéis"
        autor = "J.R.R. Tolkien"
        quantidade = 5

        with pytest.raises(ValueError):
            cadastrar_livro(
                isbn,
                titulo,
                autor,
                quantidade
            )

        MockRepository.assert_not_called()


    @patch("biblioteca.biblioteca.LivroRepository")
    def test_cadastrar_livro_existente(self, MockRepository):
        isbn = "978-3-16-148410-0"

        livro_existente = Livro(
            isbn,
            "O Senhor dos Anéis",
            "J.R.R. Tolkien",
            5
        )

        repository_mock = MockRepository.return_value

        repository_mock.buscar_por_isbn.return_value = livro_existente

        with pytest.raises(ValueError):
            cadastrar_livro(
                isbn,
                "O Senhor dos Anéis",
                "J.R.R. Tolkien",
                5
            )

        repository_mock.buscar_por_isbn.assert_called_once_with(isbn)
        repository_mock.salvar.assert_not_called()


    @patch("biblioteca.biblioteca.LivroRepository")
    def test_emprestar_livro_inexistente(self, MockRepository):
        isbn = "978-3-16-148410-0"

        repository_mock = MockRepository.return_value

        repository_mock.buscar_por_isbn.return_value = None

        with pytest.raises(ValueError):
            empestar_livro(isbn)

        repository_mock.buscar_por_isbn.assert_called_once_with(isbn)


    @patch("biblioteca.biblioteca.LivroRepository")
    def test_emprestar_livro_indisponivel(self, MockRepository):
        isbn = "978-3-16-148410-0"

        livro = Livro(
            isbn,
            "O Senhor dos Anéis",
            "J.R.R. Tolkien",
            0
        )

        repository_mock = MockRepository.return_value
        repository_mock.buscar_por_isbn.return_value = livro

        with pytest.raises(ValueError):
            empestar_livro(isbn)

        repository_mock.buscar_por_isbn.assert_called_once_with(isbn)

        repository_mock.atualizar_quantidade.assert_not_called()


    @patch("biblioteca.biblioteca.LivroRepository")
    def test_devolver_livro_inexistente(self, MockRepository):
        isbn = "978-3-16-148410-0"

        repository_mock = MockRepository.return_value
        repository_mock.buscar_por_isbn.return_value = None

        with pytest.raises(ValueError):
            devolver_livro(isbn)

        repository_mock.buscar_por_isbn.assert_called_once_with(isbn)