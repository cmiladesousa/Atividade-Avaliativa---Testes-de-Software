import pytest
import os
from unittest.mock import MagicMock
from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro
from biblioteca.database import inicializar_banco, DATABASE_NAME


#parte referente a questão 6
@pytest.fixture
def livro_valido():
    return Livro(
        isbn = "978-972-25-1763-8",
        titulo = "Carrie, a estranha",
        autor = "Stephen King",
        quantidade_disponivel = 3,
    )

@pytest.fixture
def biblioteca_mock():
    biblioteca = Biblioteca()
    biblioteca.repository = MagicMock()
    return biblioteca

#utilizando fixture 'livro_valido'
def test_disponibilidade_livro(biblioteca_mock, livro_valido):
    assert livro_valido.esta_disponivel() is True
    assert livro_valido.quantidade_disponivel == 3

def test_formatacao_livro(livro_valido):
    string = str(livro_valido)
    assert "ISBN: 978-972-25-1763-8" in string
    assert "Título: Carrie, a estranha" in string

#utilizando fixture 'biblioteca_mock'
def test_livro_consulta(biblioteca_mock, livro_valido):
    biblioteca = biblioteca_mock
    biblioteca.repository.buscar_por_isbn.return_value = livro_valido
    resultado = biblioteca.consultar_livro(livro_valido.isbn)
    assert resultado == livro_valido

def test_emprestar_livro(biblioteca_mock, livro_valido):
    biblioteca = biblioteca_mock
    biblioteca.repository.buscar_por_isbn.return_value = livro_valido
    resultado = biblioteca.emprestar_livro(livro_valido.isbn)
    assert livro_valido.quantidade_disponivel == 2
    biblioteca.repository.atualizar_quantidade.assert_called_once_with(livro_valido.isbn, 2)


#parte referente a questão 12
@pytest.fixture
def ambiente_integracao():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)

    inicializar_banco()
    biblioteca = Biblioteca()

    yield biblioteca

    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)


#cadastro, consulta, empréstimo, devolução e persistência
def test_integracao_ccedp(ambiente_integracao):
    biblioteca = ambiente_integracao
    livro = biblioteca.cadastrar_livro(
        isbn = "978-972-25-1763-8",
        titulo = "Carrie, a estranha",
        autor = "Stephen King",
        quantidade = 3,
    )

    consulta = biblioteca.consultar_livro(livro.isbn)
    assert consulta is not None
    assert consulta.isbn == livro.isbn
    assert consulta.quantidade_disponivel == 3

    biblioteca.emprestar_livro(livro.isbn)
    pos_emprestimo = biblioteca.consultar_livro(livro.isbn)

    assert pos_emprestimo.quantidade_disponivel == 2

    biblioteca.devolver_livro(livro.isbn)
    pos_devolucao = biblioteca.consultar_livro(livro.isbn)

    assert pos_devolucao.quantidade_disponivel == 3

