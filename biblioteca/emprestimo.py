from dataclasses import dataclass


@dataclass
class Emprestimo:
    id: int
    isbn: str
    usuario_id: int
    ativo: bool = True