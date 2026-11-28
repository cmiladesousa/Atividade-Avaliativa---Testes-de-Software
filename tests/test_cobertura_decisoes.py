import pytest

#disponibilidade do livro

def test_disponibilidade_false(biblioteca_teste):
    biblioteca = biblioteca_teste

    livro = biblioteca.cadastrar_livro("9722330101", "Coraline", "Neil Gaiman", 1)
    user = biblioteca.cadastrar_usuario("Alessa")

    biblioteca.emprestar_livro(livro.isbn, user.id)

    user2 = biblioteca.cadastrar_usuario("Lisa")
    with pytest.raises(ValueError):
        biblioteca.emprestar_livro(livro.isbn, user2.id)

def test_disponibilidade_true(biblioteca_teste):
    biblioteca = biblioteca_teste
    
    livro = biblioteca.cadastrar_livro("9722330101", "Coraline", "Neil Gaiman", 1)
    user = biblioteca.cadastrar_usuario("Alessa")

    resultado = biblioteca.emprestar_livro(livro.isbn, user.id)
    assert resultado.quantidade_disponivel == 0

#Multa para atrasos
def test_multa_true(biblioteca_teste):
    biblioteca = biblioteca_teste
    
    livro = biblioteca.cadastrar_livro("9722330101", "Coraline", "Neil Gaiman", 1)
    user = biblioteca.cadastrar_usuario("Alessa")

    biblioteca.emprestar_livro(livro.isbn, user.id)
    biblioteca.devolver_livro(livro.isbn, user.id, 3)

    user_consulta = biblioteca.consultar_usuario(user.id)

    assert user_consulta.multa == 6

#sem atrasos, sem multa
def test_multa_false(biblioteca_teste):
    biblioteca = biblioteca_teste
    
    livro = biblioteca.cadastrar_livro("9722330101", "Coraline", "Neil Gaiman", 1)
    user = biblioteca.cadastrar_usuario("Alessa")

    biblioteca.emprestar_livro(livro.isbn, user.id)
    biblioteca.devolver_livro(livro.isbn, user.id, 0)

    user_consulta = biblioteca.consultar_usuario(user.id)
    assert user_consulta.multa == 0