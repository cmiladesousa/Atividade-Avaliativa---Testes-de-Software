import pytest
from biblioteca.validators import validar_quantidade


def test_caminho_C01():
    assert validar_quantidade(5) == 5


def test_caminho_C02():
    with pytest.raises(ValueError):
        validar_quantidade(True)


def test_caminho_C03():
    with pytest.raises(ValueError):
        validar_quantidade(2.5)


def test_caminho_C04():
    with pytest.raises(ValueError):
        validar_quantidade(0)