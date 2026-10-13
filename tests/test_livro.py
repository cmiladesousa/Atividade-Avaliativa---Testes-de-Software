import pytest
from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro
from unittest.mock import patch
from biblioteca.validators import (validar_isbn, 
                                   validar_titulo, 
                                   validar_autor, 
                                   validar_quantidade)

def test_criacao_livro():
    #arrange
    isbn = "978-972-25-1763-8"
    titulo = "Carrie, a estranha"
    autor = "Stephen King"
    quantidade = 5

    #act
    livro = Livro(
        isbn = isbn, 
        titulo = titulo, 
        autor = autor,
        quantidade_disponivel = quantidade,
        )

    #assert
    assert livro.isbn == isbn
    assert livro.titulo == titulo
    assert livro.autor == autor
    assert livro.quantidade_disponivel == quantidade

def test_disponibilidade_livro():

    isbn = "978-972-25-1763-8"
    titulo = "Carrie, a estranha"
    autor = "Stephen King"

    #arrange
    livro_disponivel = Livro(
        isbn = isbn, 
        titulo = titulo, 
        autor = autor,
        quantidade_disponivel = 5
    )
    livro_indisponivel = Livro(
        isbn = isbn, 
        titulo = titulo, 
        autor = autor,
        quantidade_disponivel = 0
    )

    #act-assert
    assert livro_disponivel.esta_disponivel() is True
    assert livro_indisponivel.esta_disponivel() is False


def test_validar_isbn():
    isbn_valido = "978-972-25-1763-8" #arrange
    resultado = validar_isbn(isbn_valido) #act
    assert resultado == isbn_valido #assert

def test_validar_titulo():
    titulo_com_espacos = "  O Senhor dos Anéis  " #arrange
    resultado = validar_titulo(titulo_com_espacos) #act
    assert resultado == "O Senhor dos Anéis" #assert

def test_validar_autor():
    autor_com_espacos = "  Stephen King  " #arrange
    resultado = validar_autor(autor_com_espacos) #act
    assert resultado == "Stephen King" #assert

def test_validar_quantidade():
    quantidade = 5 #arrange
    resultado = validar_quantidade(quantidade) #act
    assert resultado == quantidade #assert

class TestOperacoesBiblioteca:

    @patch("biblioteca.biblioteca.LivroRepository")
    def test_cadastrar_livro(self, MockRepository):
        #arrange
        biblioteca = Biblioteca()
        repo_mock = MockRepository.return_value
        repo_mock.buscar_por_isbn.return_value = None

        #act
        livro = biblioteca.cadastrar_livro(
            isbn = "978-972-25-1763-8",
            titulo = "Carrie, a estranha",
            autor = "Stephen King",
            quantidade = 5
        
        )

        #assert
        assert livro.isbn == "978-972-25-1763-8"
        repo_mock.salvar.assert_called_once_with(livro)

        @patch("biblioteca.biblioteca.LivroRepository")
        def test_consultar_livro(self, MockRepository):
            #arrange
            livro_consultado = Livro(
                isbn = "978-972-25-1763-8", 
                titulo = "Carrie, a estranha",
                autor = "Stephen King",
                quantidade_disponivel = 5
            )
            biblioteca = Biblioteca()
            biblioteca.repository.buscar_por_isbn.return_value = livro_consultado

            #act
            resultado = biblioteca.consultar_livro("978-972-25-1763-8")

            #assert
            assert resultado == livro_consultado

        @patch("biblioteca.biblioteca.LivroRepository")
        def test_devolver_emprestar_livro(self, MockRepository):
            #arrange
            livro = Livro(
                isbn = "978-972-25-1763-8", 
                titulo = "Carrie, a estranha",
                autor = "Stephen King",
                quantidade_disponivel = 5
            )
            biblioteca = Biblioteca()
            biblioteca.repository.buscar_por_isbn.return_value = livro

            #emprestimo
            livro_emprestado = biblioteca.emprestar_livro("978-972-25-1763-8") #act
            assert livro_emprestado.quantidade_disponivel == 4 #assert

            #devolucao
            livro_devolvido = biblioteca.devolver_livro("978-972-25-1763-8") #act
            assert livro_devolvido.quantidade_disponivel == 5 #assert


