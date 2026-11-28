import pytest
from unittest.mock import Mock

@pytest.mark.parametrize("ativo, disponivel, sem_multa, esperado", [
    pytest.param(True, True, True, True, id="R1-autoriza"),
    pytest.param(True, True, False, False, id="R2-nega"),
    pytest.param(True, False, True, False, id="R3-nega"),
    pytest.param(True, False, False, False, id="R4-nega"),
    pytest.param(False, False, True, False, id="R5-nega"),
    pytest.param(False, True, True, False, id="R6-nega"),
    pytest.param(False, False, True, False, id="R7-nega"),
    pytest.param(False, False, False, False, id="R8-nega"),
])

def test_decisao_emprestimo(biblioteca_teste, monkeypatch, ativo, disponivel, sem_multa, esperado):
    biblioteca = biblioteca_teste

    user = Mock()
    user.esta_ativo.return_value = ativo
    user.possui_multa.return_value = not sem_multa

    livro = Mock()
    livro.esta_disponivel.return_value = disponivel

    monkeypatch.setattr(biblioteca, "consultar_usuario", lambda usuario_id, conexao=None: user)
    monkeypatch.setattr(biblioteca, "consultar_livro", lambda isbn, conexao=None: livro)

    resultado = biblioteca.verificar_emprestimo("9722330101", 1)

    assert resultado == esperado
