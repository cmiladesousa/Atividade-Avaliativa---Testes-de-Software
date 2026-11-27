import pytest
import sqlite3

from contextlib import closing
from biblioteca.database import conectar


ISBN = "1234567890"


def preparar_cenario(biblioteca, quantidade=5, ativo=True):
    usuario = biblioteca.cadastrar_usuario(
        "Ana", ativo=ativo
    )

    biblioteca.cadastrar_livro(
        ISBN, "Física", "Newton", quantidade
    )

    return usuario

def consultar_estado():
    with closing(conectar()) as conn:

        return {
            "livros": conn.execute(
                """
                SELECT isbn, titulo, autor, quantidade_disponivel
                FROM livros
                ORDER BY isbn
                """
            ).fetchall(),

            "usuarios": conn.execute(
                """
                SELECT id, nome, ativo, multa
                FROM usuarios
                ORDER BY id
                """
            ).fetchall(),

            "emprestimos": conn.execute(
                """
                SELECT id, isbn, usuario_id, ativo
                FROM emprestimos
                ORDER BY id
                """
            ).fetchall(),
        }


def test_cenario_emprestimo_sucesso(biblioteca_teste):
    biblioteca = biblioteca_teste
    usuario = preparar_cenario(biblioteca)

    livro = biblioteca.emprestar_livro(ISBN, usuario.id)

    assert livro.quantidade_disponivel == 4

    # Consulta novamente o livro persistido
    livro_persistido = biblioteca.consultar_livro(ISBN)

    assert livro_persistido.quantidade_disponivel == 4

    # Consulta o registro de empréstimo
    emprestimo = biblioteca.repository.buscar_emprestimo_ativo(
        ISBN, usuario.id
    )

    assert emprestimo is not None
    assert emprestimo.isbn == ISBN
    assert emprestimo.usuario_id == usuario.id
    assert emprestimo.ativo is True

    estado = consultar_estado()

    assert estado == {
        "livros": [(ISBN, "Física", "Newton", 4)],
        "usuarios": [(usuario.id, "Ana", 1, 0)],
        "emprestimos": [
            (emprestimo.id, ISBN, usuario.id, 1)
        ],
    }

    print("\nEstado persistido:", estado)

def test_cenario_livro_indisponivel(biblioteca_teste):
    biblioteca = biblioteca_teste

    usuario = preparar_cenario(biblioteca, quantidade=1)
    outro_usuario = biblioteca.cadastrar_usuario("Pedro")

    # Utiliza o único exemplar disponível
    biblioteca.emprestar_livro(ISBN, outro_usuario.id)

    estado_anterior = consultar_estado()

    with pytest.raises(
        ValueError, match="exemplares disponíveis"
    ):
        biblioteca.emprestar_livro(ISBN, usuario.id)

    livro = biblioteca.consultar_livro(ISBN)

    assert livro.quantidade_disponivel == 0

    assert biblioteca.repository.buscar_emprestimo_ativo(
        ISBN, usuario.id
    ) is None

    assert consultar_estado() == estado_anterior

    print("\nEstado preservado:", consultar_estado())

def test_cenario_multa_pendente(biblioteca_teste):
    biblioteca = biblioteca_teste
    usuario = preparar_cenario(biblioteca)

    # Gera uma multa real de R$ 10
    biblioteca.emprestar_livro(ISBN, usuario.id)

    biblioteca.devolver_livro(
        ISBN, usuario.id, dias_atraso=5
    )

    assert biblioteca.consultar_usuario(usuario.id).multa == 10

    estado_anterior = consultar_estado()

    with pytest.raises(
        ValueError, match="multas pendentes"
    ):
        biblioteca.emprestar_livro(ISBN, usuario.id)

    assert biblioteca.consultar_livro(
        ISBN
    ).quantidade_disponivel == 5

    assert biblioteca.consultar_usuario(usuario.id).multa == 10

    assert biblioteca.repository.buscar_emprestimo_ativo(
        ISBN, usuario.id
    ) is None

    assert consultar_estado() == estado_anterior

    print("\nEstado preservado:", consultar_estado())

def test_cenario_usuario_inativo(biblioteca_teste):
    biblioteca = biblioteca_teste

    usuario = preparar_cenario(
        biblioteca, ativo=False
    )

    estado_anterior = consultar_estado()

    with pytest.raises(ValueError, match="inativo"):
        biblioteca.emprestar_livro(ISBN, usuario.id)

    assert biblioteca.consultar_livro(
        ISBN
    ).quantidade_disponivel == 5

    assert biblioteca.repository.buscar_emprestimo_ativo(
        ISBN, usuario.id
    ) is None

    assert consultar_estado() == estado_anterior

    print("\nEstado preservado:", consultar_estado())

def test_cenario_isbn_inexistente(biblioteca_teste):
    biblioteca = biblioteca_teste
    usuario = preparar_cenario(biblioteca)

    isbn_inexistente = "9999999999"

    estado_anterior = consultar_estado()

    with pytest.raises(ValueError, match="não encontrado"):
        biblioteca.emprestar_livro(
            isbn_inexistente, usuario.id
        )

    assert consultar_estado() == estado_anterior

    print("\nEstado preservado:", consultar_estado())

def test_cenario_falha_persistencia(
    biblioteca_teste, monkeypatch
):
    biblioteca = biblioteca_teste
    usuario = preparar_cenario(biblioteca)

    estado_anterior = consultar_estado()

    # Guarda o método real do repositório
    registrar_original = (
        biblioteca.repository.registrar_emprestimo
    )

    def registrar_com_falha(
        isbn, usuario_id, *, conexao
    ):
        # Executa a escrita real no SQLite
        registrar_original(
            isbn,
            usuario_id,
            conexao=conexao,
        )

        # Confirma que a escrita ocorreu dentro da transação
        quantidade = conexao.execute(
            """
            SELECT quantidade_disponivel
            FROM livros
            WHERE isbn = ?
            """,
            (isbn,),
        ).fetchone()[0]

        assert quantidade == 4

        registro = conexao.execute(
            """
            SELECT COUNT(*)
            FROM emprestimos
            WHERE isbn = ? AND usuario_id = ?
            """,
            (isbn, usuario_id),
        ).fetchone()[0]

        assert registro == 1

        print("\nDentro da transação:")
        print("Estoque:", quantidade)
        print("Empréstimos registrados:", registro)

        # Simula uma falha antes do commit
        raise sqlite3.OperationalError(
            "Falha simulada de persistência"
        )

    monkeypatch.setattr(
        biblioteca.repository,
        "registrar_emprestimo",
        registrar_com_falha,
    )

    with pytest.raises(
        sqlite3.OperationalError,
        match="Falha simulada de persistência",
    ):
        biblioteca.emprestar_livro(
            ISBN, usuario.id
        )

    # Consulta novamente o estoque
    livro = biblioteca.consultar_livro(ISBN)

    assert livro.quantidade_disponivel == 5

    # Verifica se o empréstimo foi desfeito
    assert biblioteca.repository.buscar_emprestimo_ativo(
        ISBN, usuario.id
    ) is None

    # Verifica o rollback de todas as alterações
    estado_posterior = consultar_estado()

    assert estado_posterior == estado_anterior

    print("\nApós rollback:", estado_posterior)

def test_cenario_devolucao_valida(biblioteca_teste):
    biblioteca = biblioteca_teste
    usuario = preparar_cenario(biblioteca)

    biblioteca.emprestar_livro(ISBN, usuario.id)

    assert biblioteca.consultar_livro(
        ISBN
    ).quantidade_disponivel == 4

    emprestimo = biblioteca.repository.buscar_emprestimo_ativo(
        ISBN, usuario.id
    )

    assert emprestimo is not None

    livro = biblioteca.devolver_livro(
        ISBN, usuario.id, dias_atraso=5
    )

    assert livro.quantidade_disponivel == 5

    assert biblioteca.consultar_livro(
        ISBN
    ).quantidade_disponivel == 5

    assert biblioteca.consultar_usuario(usuario.id).multa == 10

    assert biblioteca.repository.buscar_emprestimo_ativo(
        ISBN, usuario.id
    ) is None

    estado = consultar_estado()

    assert estado == {
        "livros": [(ISBN, "Física", "Newton", 5)],
        "usuarios": [(usuario.id, "Ana", 1, 10)],
        "emprestimos": [
            (emprestimo.id, ISBN, usuario.id, 0)
        ],
    }

    print("\nEstado após devolução:", estado)

def test_cenario_devolucao_repetida(biblioteca_teste):
    biblioteca = biblioteca_teste
    usuario = preparar_cenario(biblioteca)

    biblioteca.emprestar_livro(ISBN, usuario.id)

    biblioteca.devolver_livro(
        ISBN, usuario.id, dias_atraso=5
    )

    estado_anterior = consultar_estado()

    with pytest.raises(
        ValueError, match="empréstimo ativo"
    ):
        biblioteca.devolver_livro(
            ISBN, usuario.id, dias_atraso=5
        )

    assert biblioteca.consultar_livro(
        ISBN
    ).quantidade_disponivel == 5

    assert biblioteca.consultar_usuario(usuario.id).multa == 10

    assert biblioteca.repository.buscar_emprestimo_ativo(
        ISBN, usuario.id
    ) is None

    assert consultar_estado() == estado_anterior

    print("\nEstado após devolução repetida:", consultar_estado())
