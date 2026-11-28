import pytest

from biblioteca import biblioteca, livro
from biblioteca.validators import validar_isbn, validar_quantidade, validar_dias_atraso


#atv2 - q2: análise de valores-limites

#teste de comprimento de isbn
@pytest.mark.parametrize("isbn, esperado", [
    ("123456789", False), #9
    ("1234567890", True), #10
    ("12345678901", False), #11
])

def test_limite_isbn(isbn, esperado):
    if esperado:
        assert validar_isbn(isbn) == isbn
    else:
        with pytest.raises(ValueError):
            validar_isbn(isbn)

#teste de exemplares
@pytest.mark.parametrize("quantidade, esperado", [
   (-1, False),
   (0, False),  
   (1, True),
   (2, True),
])

def test_limite_quantidade(quantidade, esperado):
    if esperado:
        assert validar_quantidade(quantidade) == quantidade
    else:
        with pytest.raises(ValueError):
            validar_quantidade(quantidade)

#teste de atraso
@pytest.mark.parametrize("dias_atraso, esperado", [
    (-1, False),
    (0, True),
    (1, True),
])

def test_limite_atraso(dias_atraso, esperado):
    if esperado:
        assert validar_dias_atraso(dias_atraso) == dias_atraso
    else:
        with pytest.raises(ValueError):
            validar_dias_atraso(dias_atraso)

#teste da transição de disponibilidade(emprestimo)
def test_limite_disponibilidade(biblioteca_teste):
    biblioteca = biblioteca_teste
    
    livro = biblioteca.cadastrar_livro("9722330101", "Coraline", "Neil Gaiman", 1)
    user = biblioteca.cadastrar_usuario("Alessa")

    resultado = biblioteca.emprestar_livro(livro.isbn, user.id) #act
    assert resultado.quantidade_disponivel == 0 #asssert

    user2 = biblioteca.cadastrar_usuario("Lisa")
    with pytest.raises(ValueError):
        biblioteca.emprestar_livro(livro.isbn, user2.id) #act