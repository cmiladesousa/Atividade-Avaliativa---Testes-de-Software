def validar_isbn(isbn):
    if isbn is None:
        raise ValueError("ISBN é obrigatório.")

    isbn = str(isbn).strip()

    if not isbn:
        raise ValueError("ISBN não pode estar vazio.")

    return isbn


def validar_titulo(titulo):
    if titulo is None or not titulo.strip():
        raise ValueError("Título é obrigatório.")

    return titulo.strip()


def validar_autor(autor):
    if autor is None or not autor.strip():
        raise ValueError("Autor é obrigatório.")

    return autor.strip()


def validar_quantidade(quantidade):
    if not isinstance(quantidade, int):
        raise ValueError("Quantidade deve ser um número inteiro.")

    if quantidade < 0:
        raise ValueError("Quantidade não pode ser negativa.")

    return quantidade


def validar_livro(isbn, titulo, autor, quantidade):
    return (
        validar_isbn(isbn),
        validar_titulo(titulo),
        validar_autor(autor),
        validar_quantidade(quantidade),
    )