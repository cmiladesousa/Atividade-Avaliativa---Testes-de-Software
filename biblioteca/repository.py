from contextlib import contextmanager, closing

from .database import conectar
from .livro import Livro
from .usuario import Usuario
from .emprestimo import Emprestimo

class LivroRepository:

    def __init__(self, conexao=None):
        self.conexao = conexao

    def salvar(self, livro):
        fechar_conexao = False
        conexao = self.conexao

        if conexao is None:
            conexao = conectar()
            fechar_conexao = True

        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO livros (
                isbn,
                titulo,
                autor,
                quantidade_disponivel
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                livro.isbn,
                livro.titulo,
                livro.autor,
                livro.quantidade_disponivel
            )
        )

        conexao.commit()

        if fechar_conexao:
            conexao.close()

    def buscar_por_isbn(self, isbn, *, conexao=None):

        with self._usar_conexao(conexao) as conn:

            resultado = conn.execute(
                """
                SELECT isbn, titulo, autor, quantidade_disponivel
                FROM livros
                WHERE isbn = ?
                """,
                (isbn,),
            ).fetchone()

            if resultado is None:
                return None

            return Livro(
                isbn=resultado[0],
                titulo=resultado[1],
                autor=resultado[2],
                quantidade_disponivel=resultado[3],
            )

    def atualizar_quantidade(
        self,
        isbn,
        quantidade,
        *,
        conexao=None,
    ):

        with self._usar_conexao(conexao) as conn:

            cursor = conn.execute(
                """
                UPDATE livros
                SET quantidade_disponivel = ?
                WHERE isbn = ?
                """,
                (quantidade, isbn),
            )

            if cursor.rowcount != 1:
                raise ValueError("Livro não encontrado.")

    @contextmanager
    def transacao(self):

        with closing(conectar()) as conexao:

            with conexao:

                conexao.execute("BEGIN IMMEDIATE")

                yield conexao

    @contextmanager
    def _usar_conexao(self, conexao=None):

        if conexao is not None:
            yield conexao

        else:
            with closing(conectar()) as nova_conexao:
                with nova_conexao:
                    yield nova_conexao

    def salvar_usuario(self, nome, ativo=True):

        with self._usar_conexao() as conn:

            cursor = conn.execute(
                """
                INSERT INTO usuarios (nome, ativo, multa)
                VALUES (?, ?, 0)
                """,
                (nome, int(ativo)),
            )

            return Usuario(
                id=cursor.lastrowid,
                nome=nome,
                ativo=ativo,
                multa=0,
        )

    def buscar_usuario(self, usuario_id, *, conexao=None):

        with self._usar_conexao(conexao) as conn:

            resultado = conn.execute(
                """
                SELECT id, nome, ativo, multa
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            ).fetchone()

            if resultado is None:
                return None

            return Usuario(
                id=resultado[0],
                nome=resultado[1],
                ativo=bool(resultado[2]),
                multa=resultado[3],
            )

    def registrar_emprestimo(self, isbn, usuario_id, *, conexao):

        cursor = conexao.execute(
            """
            INSERT INTO emprestimos (isbn, usuario_id, ativo)
            VALUES (?, ?, 1)
            """,
            (isbn, usuario_id),
        )

        return Emprestimo(
            id=cursor.lastrowid,
            isbn=isbn,
            usuario_id=usuario_id,
            ativo=True,
        )

    def buscar_emprestimo_ativo(
        self,
        isbn,
        usuario_id,
        *,
        conexao=None,
    ):

        with self._usar_conexao(conexao) as conn:

            resultado = conn.execute(
                """
                SELECT id, isbn, usuario_id, ativo
                FROM emprestimos
                WHERE isbn = ?
                AND usuario_id = ?
                AND ativo = 1
                ORDER BY id
                LIMIT 1
                """,
                (isbn, usuario_id),
            ).fetchone()

            if resultado is None:
                return None

            return Emprestimo(
                id=resultado[0],
                isbn=resultado[1],
                usuario_id=resultado[2],
                ativo=bool(resultado[3]),
            )

    def encerrar_emprestimo(self, emprestimo_id, *, conexao):

        cursor = conexao.execute(
            """
            UPDATE emprestimos
            SET ativo = 0
            WHERE id = ?
            AND ativo = 1
            """,
            (emprestimo_id,),
        )

        if cursor.rowcount != 1:
            raise ValueError("Empréstimo ativo não encontrado.")

    def adicionar_multa(self, usuario_id, valor, *, conexao):

        cursor = conexao.execute(
            """
            UPDATE usuarios
            SET multa = multa + ?
            WHERE id = ?
            """,
            (valor, usuario_id),
        )

        if cursor.rowcount != 1:
            raise ValueError("Usuário não encontrado.")

    def listar_todos(self):
        
        with self._usar_conexao() as conn:

            resultados = conn.execute(
                """
                SELECT isbn, titulo, autor, quantidade_disponivel
                FROM livros
                ORDER BY titulo
                """
            ).fetchall()

            livros = []

            for resultado in resultados:
                livros.append(
                    Livro(
                        isbn=resultado[0],
                        titulo=resultado[1],
                        autor=resultado[2],
                        quantidade_disponivel=resultado[3],
                    )
                )

            return livros
            
                
           