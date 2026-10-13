import pytest
from biblioteca.livro import Livro
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


def test_validar_isbn():
    isbn_valido = "978-972-25-1763-8"
    resultado = validar_isbn(isbn_valido)
    assert resultado == isbn_valido

def test_validar_titulo():
    titulo_com_espacos = "  O Senhor dos Anéis  "
    resultado = validar_titulo(titulo_com_espacos)
    assert resultado == "O Senhor dos Anéis"

def test_validar_autor():
    autor_com_espacos = "  Stephen King  "
    resultado = validar_autor(autor_com_espacos)
    assert resultado == "Stephen King"

def test_validar_quantidade():
    quantidade = 5
    resultado = validar_quantidade(quantidade)
    assert resultado == quantidade

