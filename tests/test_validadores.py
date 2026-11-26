import pytest 
from biblioteca.validators import validar_quantidade, validar_isbn, validar_dias_atraso

#referente a questão 4

@pytest.mark.parametrize(
    "quantidade, resultado_esperado",
    [
        (-10, ValueError),
        (-1, ValueError),
        (0, ValueError),
        (1, 1),
        (2, 2),
        (5, 5),
    ]
)

def test_validar_quantidade(quantidade, resultado_esperado):
    if resultado_esperado == ValueError:
        with pytest.raises(ValueError):
            validar_quantidade(quantidade)
    else:
        resultado = validar_quantidade(quantidade)
        assert resultado == resultado_esperado

#validação de isbn

@pytest.mark.parametrize(
    "input_isbn, valido, resultado_esperado",
    [
        ("123456789", False, ValueError),
        ("12345678901", False, ValueError),
        ("12345678901234", False, ValueError),
        ("123456789012A", False, ValueError),
        ("1234567890", True, "1234567890"),
        ("1234567890123", False, ValueError),
        ("978-972-25-1763-8", False, ValueError),
    ]
)

def test_validar_isbn(input_isbn, valido, resultado_esperado):
    if not valido:
        with pytest.raises(ValueError):
            validar_isbn(input_isbn)
    else:
        resultado = validar_isbn(input_isbn)
        assert resultado == resultado_esperado

def test_dias_validos():
    assert validar_dias_atraso(5) == 5

def test_dias_booleanos():
    with pytest.raises(ValueError):
        validar_dias_atraso(True)


def test_dias_decimais():
    with pytest.raises(ValueError):
        validar_dias_atraso(2.5)


def test_dias_negativos():
    with pytest.raises(ValueError):
        validar_dias_atraso(-1)