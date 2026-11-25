def validar_isbn(isbn):
    if isbn is None:
        raise ValueError("ISBN é obrigatório.")

    if not isinstance(isbn, str):
        raise ValueError("ISBN deve ser um texto.")

    isbn = isbn.strip()

    if len(isbn) != 10 or not isbn.isascii() or not isbn.isdigit():
        raise ValueError("ISBN deve conter exatamente 10 dígitos.")

    return isbn


def validar_titulo(titulo):
    if titulo is None:
        raise ValueError("Título é obrigatório.")

    if not isinstance(titulo, str):
        raise ValueError("Título deve ser um texto.")

    titulo = titulo.strip()

    if not titulo:
        raise ValueError("Título não pode ser vazio.")

    return titulo


def validar_autor(autor):
    if autor is None:
        raise ValueError("Autor é obrigatório.")

    if not isinstance(autor, str):
        raise ValueError("Autor deve ser um texto.")

    autor = autor.strip()

    if not autor:
        raise ValueError("Autor não pode ser vazio.")

    return autor


def validar_quantidade(quantidade):
    if isinstance(quantidade, bool):
        raise ValueError("A quantidade não pode ser booleana.")

    if not isinstance(quantidade, int):
        raise ValueError("A quantidade deve ser um inteiro.")

    if quantidade <= 0:
        raise ValueError("A quantidade deve ser positiva.")

    return quantidade


def validar_livro(isbn, titulo, autor, quantidade):
    return (
        validar_isbn(isbn),
        validar_titulo(titulo),
        validar_autor(autor),
        validar_quantidade(quantidade),
    )


def validar_dias_atraso(dias_atraso):
    if isinstance(dias_atraso, bool):
        raise ValueError("Os dias de atraso não podem ser booleanos.")

    if not isinstance(dias_atraso, int):
        raise ValueError("Os dias de atraso devem ser inteiros.")

    if dias_atraso < 0:
        raise ValueError("Os dias de atraso não podem ser negativos.")

    return dias_atraso