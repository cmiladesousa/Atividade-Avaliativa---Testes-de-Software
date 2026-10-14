import pytest 
from biblioteca.validators import validar_titulo, validar_autor, validar_livro
from biblioteca.livro import Livro

def test_titulo_vazio():
    with pytest.raises(ValueError, match="Título é obrigatório"):
        validar_titulo("")

def test_autor_vazio():
    with pytest.raises(ValueError, match="Autor é obrigatório"):
            validar_autor("")

def test_livro_completo():
    resultado = validar_livro('978-972-25-1763-8', 'Carrie, a estranha', 'Stephen King', 3)
    assert resultado == ('978-972-25-1763-8', 'Carrie, a estranha', 'Stephen King', 3)