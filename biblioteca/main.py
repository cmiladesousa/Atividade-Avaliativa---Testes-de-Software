import sqlite3

from .biblioteca import Biblioteca
from .database import inicializar_banco


def mostrar_menu():
    print("\n===== MINI SISTEMA DE BIBLIOTECA =====")
    print("1 - Cadastrar livro")
    print("2 - Consultar livro")
    print("3 - Verificar disponibilidade")
    print("4 - Realizar empréstimo")
    print("5 - Realizar devolução")
    print("6 - Listar livros")
    print("7 - Cadastrar usuário")
    print("8 - Consultar usuário")
    print("9 - Verificar possibilidade de empréstimo")
    print("10 - Verificar multa pendente")
    print("11 - Calcular multa")
    print("12 - Quitar multa")
    print("0 - Sair")


def main():
    inicializar_banco()

    biblioteca = Biblioteca()

    while True:
        mostrar_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        try:

            # Cadastro de livro
            if opcao == "1":
                isbn = input("ISBN: ")
                titulo = input("Título: ")
                autor = input("Autor: ")
                quantidade = int(
                    input("Quantidade de exemplares: ")
                )

                livro = biblioteca.cadastrar_livro(
                    isbn,
                    titulo,
                    autor,
                    quantidade,
                )

                print("\nLivro cadastrado com sucesso!")
                print(livro)

            # Consulta de livro
            elif opcao == "2":
                isbn = input("ISBN: ")

                livro = biblioteca.consultar_livro(isbn)

                print()
                print(livro)

            # Verificação de disponibilidade
            elif opcao == "3":
                isbn = input("ISBN: ")

                disponivel = biblioteca.verificar_disponibilidade(
                    isbn
                )

                if disponivel:
                    print("Livro disponível para empréstimo.")
                else:
                    print("Livro indisponível.")

            # Realização de empréstimo
            elif opcao == "4":
                isbn = input("ISBN: ")
                usuario_id = int(input("ID do usuário: "))

                livro = biblioteca.emprestar_livro(
                    isbn,
                    usuario_id,
                )

                print("\nEmpréstimo realizado com sucesso.")
                print(
                    f"Exemplares restantes: "
                    f"{livro.quantidade_disponivel}"
                )

            # Realização de devolução
            elif opcao == "5":
                isbn = input("ISBN: ")
                usuario_id = int(input("ID do usuário: "))

                dias_atraso = int(
                    input("Quantidade de dias de atraso: ")
                )

                livro = biblioteca.devolver_livro(
                    isbn,
                    usuario_id,
                    dias_atraso,
                )

                multa = biblioteca.calcular_multa(dias_atraso)

                print("\nDevolução realizada com sucesso.")
                print(
                    f"Exemplares disponíveis: "
                    f"{livro.quantidade_disponivel}"
                )

                if multa > 0:
                    print(f"Multa aplicada: R$ {multa:.2f}")
                else:
                    print("Nenhuma multa aplicada.")

            # Listagem de livros
            elif opcao == "6":
                livros = biblioteca.listar_livros()

                if not livros:
                    print("Nenhum livro cadastrado.")

                for livro in livros:
                    print("\n----------------------")
                    print(livro)

            # Cadastro de usuário
            elif opcao == "7":
                nome = input("Nome do usuário: ")

                situacao = input(
                    "Usuário ativo? (S/N): "
                ).strip().upper()

                if situacao not in ("S", "N"):
                    raise ValueError(
                        "Informe S para ativo ou N para inativo."
                    )

                ativo = situacao == "S"

                usuario = biblioteca.cadastrar_usuario(
                    nome,
                    ativo,
                )

                print("\nUsuário cadastrado com sucesso!")
                print(f"ID: {usuario.id}")
                print(f"Nome: {usuario.nome}")
                print(
                    f"Situação: "
                    f"{'Ativo' if usuario.ativo else 'Inativo'}"
                )

            # Consulta de usuário
            elif opcao == "8":
                usuario_id = int(input("ID do usuário: "))

                usuario = biblioteca.consultar_usuario(
                    usuario_id
                )

                print("\n===== DADOS DO USUÁRIO =====")
                print(f"ID: {usuario.id}")
                print(f"Nome: {usuario.nome}")
                print(
                    f"Situação: "
                    f"{'Ativo' if usuario.ativo else 'Inativo'}"
                )
                print(f"Multa pendente: R$ {usuario.multa:.2f}")

            # Verificação da possibilidade de empréstimo
            elif opcao == "9":
                isbn = input("ISBN: ")
                usuario_id = int(input("ID do usuário: "))

                permitido = biblioteca.verificar_emprestimo(
                    isbn,
                    usuario_id,
                )

                if permitido:
                    print("\nEmpréstimo permitido.")

                else:
                    print("\nEmpréstimo não permitido.")

            # Verificação de multa pendente
            elif opcao == "10":
                usuario_id = int(input("ID do usuário: "))

                possui_multa = biblioteca.verificar_multa(
                    usuario_id
                )

                if possui_multa:
                    usuario = biblioteca.consultar_usuario(
                        usuario_id
                    )

                    print("\nO usuário possui multa pendente.")
                    print(
                        f"Valor total: R$ {usuario.multa:.2f}"
                    )

                else:
                    print("\nO usuário não possui multas pendentes.")

            # Cálculo de multa
            elif opcao == "11":
                dias_atraso = int(
                    input("Quantidade de dias de atraso: ")
                )

                multa = biblioteca.calcular_multa(
                    dias_atraso
                )

                print(f"\nDias de atraso: {dias_atraso}")
                print(f"Valor da multa: R$ {multa:.2f}")

            # Quitar multa
            elif opcao == "12":
                usuario_id = int(input("ID do usuário: "))

                usuario = biblioteca.consultar_usuario(usuario_id)

                print(f"Multa pendente: R$ {usuario.multa:.2f}")

                confirmacao = input(
                    "Confirmar pagamento? (S/N): "
                ).strip().upper()

                if confirmacao == "S":

                    valor_pago = biblioteca.quitar_multa(usuario_id)

                    print("\nMulta quitada com sucesso!")
                    print(f"Valor pago: R$ {valor_pago:.2f}")

                elif confirmacao == "N":
                    print("Pagamento cancelado.")

                else:
                    print("Opção inválida.")

            # Encerramento
            elif opcao == "0":
                print("Sistema encerrado.")
                break

            else:
                print("Opção inválida.")

        except ValueError as erro:
            print(f"\nErro: {erro}")

        except sqlite3.Error as erro:
            print(f"\nErro de persistência: {erro}")

        except Exception as erro:
            print(f"\nErro inesperado: {erro}")


if __name__ == "__main__":
    main()