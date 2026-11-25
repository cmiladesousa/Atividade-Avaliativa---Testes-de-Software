import pytest

from biblioteca.biblioteca import Biblioteca
from biblioteca import database


@pytest.fixture
def biblioteca_teste(tmp_path, monkeypatch):

    caminho_banco = tmp_path / "biblioteca_teste.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(caminho_banco),
    )

    database.inicializar_banco()

    return Biblioteca()