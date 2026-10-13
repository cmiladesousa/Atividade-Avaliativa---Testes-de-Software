import pytest
import sqlite3
from unittest.mock import MagicMock
from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro

#referente a questão 8

class TestBibliotecaSideEffect:

    def test_cadastrar_livro(self):
        biblioteca = Biblioteca()
        biblioteca.repository = MagicMock()

        biblioteca.repository.salvar.side_effect = [None, sqlite3.IntegrityError("Livro já existe no banco de dados")]
        # 1ª chamada: retorna None e permite cadastro
        # 2ª chamada: simula erro pois livro já eixtse

        biblioteca.repository.buscar_por_isbn.return_value = None

        #cenário 1 - sucesso
        livro1 = biblioteca.cadastrar_livro(
            isbn = "978-972-25-1763-8",
            titulo = "Carrie, a estranha",
            autor = "Stephen King",
            quantidade = 3,
        )

        assert livro1.isbn == "978-972-25-1763-8"
        assert biblioteca.repository.salvar.call_count == 1

        #cenário 2 - falha
        with pytest.raises(ValueError, match="Já existe um livro cadastrado"):
            biblioteca.cadastrar_livro(
                isbn = "978-972-25-1763-8",
                        titulo = "Carrie, a estranha",
                        autor = "Stephen King",
                        quantidade = 3,
            )

        assert biblioteca.repository.salvar.call_count == 2

    def test_consultar_livro(self):
        biblioteca = Biblioteca()
        biblioteca.repository = MagicMock()

        livro_encontrado = Livro(
            isbn = "978-972-25-1763-8",
            titulo = "Carrie, a estranha",
            autor = "Stephen King",
            quantidade_disponivel = 3,
        )

        biblioteca.repository.buscar_por_isbn.side_effect = [livro_encontrado, None]

        res_sucesso = biblioteca.consultar_livro("978-972-25-1763-8")
        assert res_sucesso == livro_encontrado

        with pytest.raises(ValueError, match="não encontrado"):
            biblioteca.consultar_livro("978-972-25-1763-8")




