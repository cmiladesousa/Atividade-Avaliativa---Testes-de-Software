# Mini Sistema de Biblioteca

Projeto desenvolvido para a atividade avaliativa da disciplina **Testes de Software I**, com o objetivo de implementar um Mini Sistema de Biblioteca e aplicar conceitos de testes unitários, testes de integração, persistência e cobertura de testes.

O sistema permite cadastrar, consultar, emprestar e devolver livros, além de controlar a quantidade de exemplares disponíveis.

## Tecnologias

- Python
- Pytest
- Unittest
- SQLite

## Estrutura do projeto

```text
.
├── biblioteca/
│   ├── biblioteca.py
│   ├── database.py
│   ├── livro.py
│   ├── main.py
│   ├── repository.py
│   └── validators.py
│
├── tests/
│   ├── test_biblioteca.py
│   ├── test_integracao.py
│   ├── test_livro.py
│   ├── test_repository.py
│   └── test_validadores.py
│
├── tests_unittest/
│   ├── test_biblioteca_unittest.py
│   └── test_validadores_unittest.py
│
├── biblioteca.db
└── README.md