import pytest


def verificar_cadastro(biblioteca, campo, valor, valido):
    dados = {
        "isbn": "1234567890",
        "titulo": "Introdução à Física",
        "autor": "Autor Exemplo",
        "quantidade": 5,
    }

    dados[campo] = valor

    if valido:
        livro = biblioteca.cadastrar_livro(**dados)

        assert livro.isbn == dados["isbn"]
        assert livro.titulo == dados["titulo"]
        assert livro.autor == dados["autor"]
        assert livro.quantidade_disponivel == dados["quantidade"]

        livro_persistido = biblioteca.consultar_livro(
            dados["isbn"]
        )

        assert livro_persistido.isbn == dados["isbn"]
        assert livro_persistido.titulo == dados["titulo"]
        assert livro_persistido.autor == dados["autor"]
        assert (
            livro_persistido.quantidade_disponivel
            == dados["quantidade"]
        )

    else:
        estado_anterior = biblioteca.listar_livros()

        with pytest.raises(ValueError):
            biblioteca.cadastrar_livro(**dados)

        assert biblioteca.listar_livros() == estado_anterior

@pytest.mark.parametrize(
    "valor, valido",
    [
        pytest.param("1234567890", True, id="ISBN-01"),
        pytest.param("0123456789", True, id="ISBN-02"),
        pytest.param(1234567890, False, id="ISBN-03"),
        pytest.param(1234567890.0, False, id="ISBN-04"),
        pytest.param(True, False, id="ISBN-05"),
        pytest.param(None, False, id="ISBN-06"),
        pytest.param("", False, id="ISBN-07"),
        pytest.param("   ", False, id="ISBN-08"),
        pytest.param("123456789", False, id="ISBN-09"),
        pytest.param("12345678901", False, id="ISBN-10"),
        pytest.param("123456789A", False, id="ISBN-11"),
        pytest.param("12345-6789", False, id="ISBN-12"),
        pytest.param("12345 6789", False, id="ISBN-13"),
    ],
)
def test_equivalencia_isbn(biblioteca_teste, valor, valido):
    verificar_cadastro(
        biblioteca_teste, "isbn", valor, valido
    )

@pytest.mark.parametrize(
    "valor, valido",
    [
        pytest.param("Introdução à Física", True, id="TIT-01"),
        pytest.param("A", True, id="TIT-02"),
        pytest.param("Física 2: Teoria e Prática", True, id="TIT-03"),
        pytest.param(123, False, id="TIT-04"),
        pytest.param(1.5, False, id="TIT-05"),
        pytest.param(True, False, id="TIT-06"),
        pytest.param(None, False, id="TIT-07"),
        pytest.param("", False, id="TIT-08"),
        pytest.param("   ", False, id="TIT-09"),
    ],
)
def test_equivalencia_titulo(biblioteca_teste, valor, valido):
    verificar_cadastro(
        biblioteca_teste, "titulo", valor, valido
    )


@pytest.mark.parametrize(
    "valor, valido",
    [
        pytest.param("Isaac Newton", True, id="AUT-01"),
        pytest.param("A", True, id="AUT-02"),
        pytest.param("José A. da Silva", True, id="AUT-03"),
        pytest.param(123, False, id="AUT-04"),
        pytest.param(1.5, False, id="AUT-05"),
        pytest.param(True, False, id="AUT-06"),
        pytest.param(None, False, id="AUT-07"),
        pytest.param("", False, id="AUT-08"),
        pytest.param("   ", False, id="AUT-09"),
    ],
)
def test_equivalencia_autor(biblioteca_teste, valor, valido):
    verificar_cadastro(
        biblioteca_teste, "autor", valor, valido
    )

@pytest.mark.parametrize(
    "valor, valido",
    [
        pytest.param(5, True, id="QTD-01"),
        pytest.param(1, True, id="QTD-02"),
        pytest.param(0, False, id="QTD-03"),
        pytest.param(-1, False, id="QTD-04"),
        pytest.param(2.5, False, id="QTD-05"),
        pytest.param(5.0, False, id="QTD-06"),
        pytest.param("5", False, id="QTD-07"),
        pytest.param("cinco", False, id="QTD-08"),
        pytest.param(True, False, id="QTD-09"),
        pytest.param(False, False, id="QTD-10"),
        pytest.param(None, False, id="QTD-11"),
        pytest.param("", False, id="QTD-12"),
    ],
)
def test_equivalencia_quantidade(biblioteca_teste, valor, valido):
    verificar_cadastro(
        biblioteca_teste, "quantidade", valor, valido
    )