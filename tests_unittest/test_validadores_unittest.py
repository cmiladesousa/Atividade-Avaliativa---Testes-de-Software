import unittest
from biblioteca.validators import (
    validar_isbn,
    validar_titulo,
    validar_quantidade
)

class TestValidadores(unittest.TestCase):
    def test_validar_isbn_valido(self):
        isbn = "978-3-16-148410-0"
        resultado = validar_isbn(isbn)
        self.assertEqual(resultado, isbn)

    def test_validar_isbn_invalido(self):
        isbn = "978-3-16-148410-0a"
        with self.assertRaises(ValueError):
            validar_isbn(isbn)

    def test_validar_titulo_valido(self):
        titulo = "   O Senhor dos Anéis   "
        resultado = validar_titulo(titulo)
        self.assertEqual(resultado, "O Senhor dos Anéis")

    def test_validar_titulo_invalido(self):
        titulo = "   "
        with self.assertRaises(ValueError):
            validar_titulo(titulo)

    def test_validar_quantidade_valida(self):
        quantidade = 5
        resultado = validar_quantidade(quantidade)
        self.assertEqual(resultado, quantidade)

    def test_validar_quantidade_invalida(self):
        quantidade = -5
        with self.assertRaises(ValueError):
            validar_quantidade(quantidade)

if __name__ == "__main__":
    unittest.main()