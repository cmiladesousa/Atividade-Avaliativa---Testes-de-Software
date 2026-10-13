import pytest 
from biblioteca.validators import validar_quantidade, validar_isbn

#referente a questão 4

@pytest.mark.parametrize(
    "quantidade, resultado_esperado",
    [
        (-10, ValueError),
        (-1, ValueError),
        (0, 0),
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
        ("123456789", False, ValueError), #9 digitos
        ("12345678901", False, ValueError), #11 digitos
        ("12345678901234", False, ValueError), #14 digitos
        ("123456789012A", False, ValueError), #deve conter apenas numeros e/ou traços
        ("1234567890", True, "1234567890"), #10 digitos sem tracos
        ("1234567890123", True, "1234567890123"), #13 digitos sem tracos
        ("978-972-25-1763-8", True, "978-972-25-1763-8"), #13 digitos com tracos
    ]
)

def test_validar_isbn(input_isbn, valido, resultado_esperado):
    if not valido:
        with pytest.raises(ValueError):
            validar_isbn(input_isbn)
    else:
        resultado = validar_isbn(input_isbn)
        assert resultado == resultado_esperado