import pytest

from contextlib import nullcontext
from unittest.mock import Mock

from biblioteca.biblioteca import Biblioteca


@pytest.mark.parametrize(
    "ativo, disponivel, sem_multa, esperado, avaliacoes",
    [
        pytest.param(
            True, True, True, True,
            ["A", "B", "C"],
            id="T01"
        ),

        pytest.param(
            False, True, True, False,
            ["A"],
            id="T02"
        ),

        pytest.param(
            True, False, True, False,
            ["A", "B"],
            id="T03"
        ),

        pytest.param(
            True, True, False, False,
            ["A", "B", "C"],
            id="T04"
        ),
    ]
)
def test_cobertura_condicoes_emprestimo(
    ativo,
    disponivel,
    sem_multa,
    esperado,
    avaliacoes,
):

    visitadas = []

    # Objetos simulados
    repository = Mock()
    usuario = Mock()
    livro = Mock()

    repository.transacao.return_value = nullcontext(Mock())

    biblioteca = Biblioteca(repository)

    biblioteca.consultar_usuario = Mock(return_value=usuario)
    biblioteca.consultar_livro = Mock(return_value=livro)

    # Condição A
    def verificar_ativo():
        visitadas.append("A")
        return ativo

    # Condição B
    def verificar_disponivel():
        visitadas.append("B")
        return disponivel

    # Condição C
    def verificar_multa():
        visitadas.append("C")
        return not sem_multa

    usuario.esta_ativo.side_effect = verificar_ativo

    livro.esta_disponivel.side_effect = verificar_disponivel

    usuario.possui_multa.side_effect = verificar_multa

    # Executa a função real
    resultado = biblioteca.verificar_emprestimo(
        "1234567890",
        1,
    )

    # Verifica a decisão global
    assert resultado is esperado

    # Verifica as condições efetivamente avaliadas
    assert visitadas == avaliacoes

    print(f"\nCondições avaliadas: {visitadas}")
    print(f"Decisão global: {resultado}")