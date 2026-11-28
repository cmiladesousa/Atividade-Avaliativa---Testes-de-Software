import sqlite3

from .livro import Livro
from .repository import LivroRepository
from .validators import validar_dias_atraso, validar_livro, validar_isbn


class Biblioteca:

    def __init__(self, repository=None):
        if repository is None:
            repository = LivroRepository()

        self.repository = repository

    def cadastrar_livro(self, isbn, titulo, autor, quantidade):
        isbn, titulo, autor, quantidade = validar_livro(
            isbn,
            titulo,
            autor,
            quantidade,
        )

        if self.repository.buscar_por_isbn(isbn):
            raise ValueError(
                f"Já existe um livro cadastrado com o ISBN {isbn}."
            )

        livro = Livro(
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            quantidade_disponivel=quantidade,
        )

        try:
            self.repository.salvar(livro)

        except sqlite3.IntegrityError:
            raise ValueError(
                f"Já existe um livro cadastrado com o ISBN {isbn}."
            )

        return livro

    def consultar_livro(self, isbn, *, conexao=None):

        isbn = validar_isbn(isbn)

        if conexao is None:
            livro = self.repository.buscar_por_isbn(isbn)
        else:
            livro = self.repository.buscar_por_isbn(
                isbn,
                conexao=conexao,
            )

        if livro is None:
            raise ValueError(
                f"Livro com ISBN {isbn} não encontrado."
            )

        return livro

    def verificar_disponibilidade(self, isbn):
        livro = self.consultar_livro(isbn)

        return livro.esta_disponivel()
    
    def emprestar_livro(self, isbn, usuario_id):

        with self.repository.transacao() as conexao:

            livro = self.consultar_livro(
                isbn,
                conexao=conexao,
            )

            usuario = self.consultar_usuario(
                usuario_id,
                conexao=conexao,
            )

            if not usuario.esta_ativo():
                raise ValueError(
                    "O usuário está inativo."
                )

            if not livro.esta_disponivel():
                raise ValueError(
                    f"Não há exemplares disponíveis de '{livro.titulo}'."
                )

            if usuario.possui_multa():
                raise ValueError(
                    "O usuário possui multas pendentes."
                )

            nova_quantidade = livro.quantidade_disponivel - 1

            self.repository.atualizar_quantidade(
                livro.isbn,
                nova_quantidade,
                conexao=conexao,
            )

            self.repository.registrar_emprestimo(
                livro.isbn,
                usuario.id,
                conexao=conexao,
            )

        livro.quantidade_disponivel = nova_quantidade

        return livro
    
    """
    # Parte referente a questão 13
    # Versão com erro proposital para teste de integração, com decremento de 2 exemplares ao invés de 1
    def emprestar_livro(self, isbn):
        livro = self.consultar_livro(isbn)
    
        if not livro.esta_disponivel():
            raise ValueError(
                f"Não há exemplares disponíveis de '{livro.titulo}'."
            )
    
        livro.quantidade_disponivel -= 2
    
        self.repository.atualizar_quantidade(
            livro.isbn,
            livro.quantidade_disponivel,
        )
    
        return livro
    """
    def calcular_multa(self, dias_atraso):

        dias_atraso = validar_dias_atraso(dias_atraso)

        return dias_atraso * 2

    def devolver_livro(self, isbn, usuario_id, dias_atraso=0):

        multa = self.calcular_multa(dias_atraso)

        with self.repository.transacao() as conexao:

            livro = self.consultar_livro(
                isbn,
                conexao=conexao,
            )

            usuario = self.consultar_usuario(
                usuario_id,
                conexao=conexao,
            )

            emprestimo = self.repository.buscar_emprestimo_ativo(
                livro.isbn,
                usuario.id,
                conexao=conexao,
            )

            if emprestimo is None:
                raise ValueError(
                    "Não existe empréstimo ativo correspondente."
                )

            nova_quantidade = livro.quantidade_disponivel + 1

            self.repository.encerrar_emprestimo(
                emprestimo.id,
                conexao=conexao,
            )

            self.repository.atualizar_quantidade(
                livro.isbn,
                nova_quantidade,
                conexao=conexao,
            )

            if multa > 0:
                self.repository.adicionar_multa(
                    usuario.id,
                    multa,
                    conexao=conexao,
                )

        livro.quantidade_disponivel = nova_quantidade

        return livro

    def listar_livros(self):
        return self.repository.listar_todos()

    #contagem_livros_disponiveis: criado para a questão 8:
    def contagem_livros_disponiveis(self):
        total = 0
        for livro in self.listar_livros():
            if livro.esta_disponivel():
                total += 1
        return total

    def cadastrar_usuario(self, nome, ativo=True):

        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome do usuário não pode ser vazio.")

        if not isinstance(ativo, bool):
            raise ValueError("A situação do usuário deve ser booleana.")

        return self.repository.salvar_usuario(
            nome.strip(),
            ativo,
        )

    def consultar_usuario(self, usuario_id, *, conexao=None):

        if (
            isinstance(usuario_id, bool)
            or not isinstance(usuario_id, int)
            or usuario_id <= 0
        ):
            raise ValueError("Identificador de usuário inválido.")

        usuario = self.repository.buscar_usuario(
            usuario_id,
            conexao=conexao,
        )

        if usuario is None:
            raise ValueError(
                f"Usuário {usuario_id} não encontrado."
            )

        return usuario

    def verificar_multa(self, usuario_id):

        usuario = self.consultar_usuario(usuario_id)

        return usuario.possui_multa()

    def verificar_emprestimo(self, isbn, usuario_id):

        with self.repository.transacao() as conexao:

            livro = self.consultar_livro(
                isbn,
                conexao=conexao,
            )

            usuario = self.consultar_usuario(
                usuario_id,
                conexao=conexao,
            )

            return (
                usuario.esta_ativo()
                and livro.esta_disponivel()
                and not usuario.possui_multa()
            )
    def quitar_multa(self, usuario_id):

        with self.repository.transacao() as conexao:

            usuario = self.consultar_usuario(
                usuario_id,
                conexao=conexao,
            )

            if not usuario.possui_multa():
                raise ValueError(
                    "O usuário não possui multas pendentes."
                )

            valor_pago = usuario.multa

            self.repository.quitar_multa(
                usuario.id,
                conexao=conexao,
            )

        return valor_pago
    