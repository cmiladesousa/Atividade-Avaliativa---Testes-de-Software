import pytest

from itertools import combinations, product


casos = [
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
]


def test_cobertura_dos_pares():

    for i, j in combinations(range(3), 2):

        pares_cobertos = {
            (c[i], c[j]) for c in casos
        }

        pares_esperados = set(
            product([0, 1], repeat=2)
        )

        assert pares_cobertos == pares_esperados


@pytest.mark.parametrize(
    "a, b, c",
    casos,
    ids=["CT01", "CT04", "CT06", "CT07"],
)
def test_cadastro_pares(biblioteca_teste, a, b, c):

    biblioteca = biblioteca_teste

    isbn = ["1234567890", "123456789"][a]
    titulo = ["Física", ""][b]
    quantidade = [5, 0][c]
    autor = "Newton"

    # Estado inicial do banco
    assert biblioteca.listar_livros() == []

    # Todos os fatores são válidos
    if (a, b, c) == (0, 0, 0):

        livro = biblioteca.cadastrar_livro(
            isbn, titulo, autor, quantidade
        )

        assert livro.isbn == isbn
        assert livro.titulo == titulo
        assert livro.autor == autor
        assert livro.quantidade_disponivel == quantidade

        # Verifica a persistência
        livro_persistido = biblioteca.consultar_livro(isbn)

        assert livro_persistido.isbn == isbn
        assert livro_persistido.titulo == titulo
        assert livro_persistido.autor == autor
        assert livro_persistido.quantidade_disponivel == quantidade

        assert len(biblioteca.listar_livros()) == 1

    else:

        with pytest.raises(ValueError):
            biblioteca.cadastrar_livro(
                isbn, titulo, autor, quantidade
            )

        # Verifica que entradas inválidas não persistem
        assert biblioteca.listar_livros() == []