import pytest

@pytest.mark.parametrize("quantidade, esperado", [
    pytest.param([], 0, id="lista_vazia"),
    pytest.param([3], 1, id="livro_disponivel"),
    pytest.param([3, 1, 4, 5], 4, id="varios_livros"),
    ], 
)

def test_contagem_livros_disponiveis(biblioteca_teste, quantidade, esperado):
    for i, qtnd in enumerate(quantidade):
        biblioteca_teste.cadastrar_livro(f"123456789{i}", f"Livro {i}", f"Autor {i}", qtnd)

    resultado = biblioteca_teste.contagem_livros_disponiveis()
    assert resultado == esperado