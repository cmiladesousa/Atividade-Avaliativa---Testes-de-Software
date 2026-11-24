from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    nome: str
    ativo: bool = True
    multa: int = 0

    def possui_multa(self):
        return self.multa > 0

    def esta_ativo(self):
        return self.ativo