import pytest
import sqlite3
import os
from biblioteca.livro import Livro
from biblioteca.biblioteca import Biblioteca
from biblioteca.repository import LivroRepository
from biblioteca.database import inicializar_banco, DATABASE_NAME

#referente a questão 9
@pytest.fixture
def biblioteca_teste(tmp_path):
    caminho_banco = tmp_path / "biblioteca_teste.db"

    conexao = sqlite3.connect(caminho_banco)

    inicializar_banco(conexao)

    repository = LivroRepository(conexao)

    biblioteca = Biblioteca(repository)

    yield biblioteca

    conexao.close()

def test_fluxo_completo_biblioteca(biblioteca_teste):
    biblioteca = biblioteca_teste
    livro_cadastrado = biblioteca.cadastrar_livro(
        "978-3-16-148410-0",
        "O Senhor dos Anéis",
        "J.R.R. Tolkien",
        5
    )

    assert livro_cadastrado.isbn == "978-3-16-148410-0"
    assert livro_cadastrado.titulo == "O Senhor dos Anéis"
    assert livro_cadastrado.autor == "J.R.R. Tolkien"
    assert livro_cadastrado.quantidade_disponivel == 5


    livro_consultado = biblioteca.consultar_livro(
        "978-3-16-148410-0"
    )

    assert livro_consultado is not None
    assert livro_consultado.isbn == "978-3-16-148410-0"
    assert livro_consultado.quantidade_disponivel == 5


    biblioteca.emprestar_livro(
        "978-3-16-148410-0"
    )


    livro_apos_emprestimo = biblioteca.consultar_livro(
        "978-3-16-148410-0"
    )

    assert livro_apos_emprestimo.quantidade_disponivel == 4


    biblioteca.devolver_livro(
        "978-3-16-148410-0"
    )


    livro_apos_devolucao = biblioteca.consultar_livro(
        "978-3-16-148410-0"
    )

    assert livro_apos_devolucao.quantidade_disponivel == 5

#referente a questão 10

class TesteBibliotecaIntegracao:

    @pytest.fixture(autouse=True)
    def banco_de_testes(self):
        if os.path.exists(DATABASE_NAME):
            os.remove(DATABASE_NAME)
        inicializar_banco()

        yield

        if os.path.exists(DATABASE_NAME):
            os.remove(DATABASE_NAME)

    def test_biblioteca_integracao(self):
        biblioteca = Biblioteca()

        #cadastro
        livro = biblioteca.cadastrar_livro(
            isbn = "978-972-25-1763-8",
            titulo = "Carrie, a estranha",
            autor = "Stephen King",
            quantidade = 3,
        )

        assert livro.isbn == livro.isbn
        assert livro.quantidade_disponivel == 3

        consulta = biblioteca.consultar_livro(livro.isbn)
        assert consulta is not None
        assert consulta.titulo == livro.titulo
        assert consulta.autor == livro.autor
        assert consulta.quantidade_disponivel == 3

        emprestimo = biblioteca.emprestar_livro(livro.isbn)
        assert emprestimo.quantidade_disponivel == 2

        pos_emprestimo = biblioteca.consultar_livro(livro.isbn)
        assert pos_emprestimo.quantidade_disponivel == 2

        devolucao = biblioteca.devolver_livro(livro.isbn)
        assert devolucao.quantidade_disponivel == 3

        pos_devolucao = biblioteca.consultar_livro(livro.isbn)
        assert pos_devolucao.quantidade_disponivel == 3

#referente a questão 11
@pytest.fixture
def banco_teste(tmp_path):
    caminho_banco = tmp_path / "biblioteca_teste.db"

    conexao = sqlite3.connect(caminho_banco)

    inicializar_banco(conexao)

    conexao.close()

    return caminho_banco

def test_persistencia_livro(banco_teste):
    # ARRANGE
    livro = Livro(
        isbn="978-3-16-148410-0",
        titulo="O Senhor dos Anéis",
        autor="J.R.R. Tolkien",
        quantidade_disponivel=5
    )

    conexao = sqlite3.connect(banco_teste)

    repository = LivroRepository(conexao)

    repository.salvar(livro)

    conexao.close()

    conexao = sqlite3.connect(banco_teste)

    novo_repository = LivroRepository(conexao)

    # ACT
    livro_recuperado = novo_repository.buscar_por_isbn(
        "978-3-16-148410-0"
    )

    conexao.close()

    assert livro_recuperado is not None

    assert livro_recuperado.isbn == livro.isbn
    assert livro_recuperado.titulo == livro.titulo
    assert livro_recuperado.autor == livro.autor
    assert (
        livro_recuperado.quantidade_disponivel
        == livro.quantidade_disponivel
    )