class Livro:
    def __init__(self, isbn, titulo, autor, quantidade_disponivel):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.quantidade_disponivel = quantidade_disponivel

    def esta_disponivel(self):
        return self.quantidade_disponivel > 0

    def __str__(self):
        return (
            f"ISBN: {self.isbn}\n"
            f"Título: {self.titulo}\n"
            f"Autor: {self.autor}\n"
            f"Disponíveis: {self.quantidade_disponivel}"
        )