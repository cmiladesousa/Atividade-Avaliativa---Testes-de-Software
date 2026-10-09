import unittest
from unittest.mock import patch

from biblioteca.biblioteca import cadastrar_livro


class TestBiblioteca(unittest.TestCase):

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

        self.assertEqual(livro.isbn, isbn)
        self.assertEqual(livro.titulo, titulo)
        self.assertEqual(livro.autor, autor)
        self.assertEqual(
            livro.quantidade_disponivel,
            quantidade
        )

        repository_mock.buscar_por_isbn.assert_called_once_with(
            isbn
        )

        repository_mock.salvar.assert_called_once_with(livro)


    def test_cadastrar_livro_invalido(self):
        isbn = "978-3-16-148410-0a"
        titulo = "O Senhor dos Anéis"
        autor = "J.R.R. Tolkien"
        quantidade = 5

        with self.assertRaises(ValueError):
            cadastrar_livro(
                isbn,
                titulo,
                autor,
                quantidade
            )


if __name__ == "__main__":
    unittest.main()