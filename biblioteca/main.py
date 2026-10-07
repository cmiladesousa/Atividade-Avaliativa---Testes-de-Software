from biblioteca import Biblioteca
from database import inicializar_banco


def mostrar_menu():
    print("\n===== MINI SISTEMA DE BIBLIOTECA =====")
    print("1 - Cadastrar livro")
    print("2 - Consultar livro")
    print("3 - Verificar disponibilidade")
    print("4 - Realizar empréstimo")
    print("5 - Realizar devolução")
    print("6 - Listar livros")
    print("0 - Sair")


def main():
    inicializar_banco()

    biblioteca = Biblioteca()

    while True:
        mostrar_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        try:

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

            elif opcao == "2":
                isbn = input("ISBN: ")

                livro = biblioteca.consultar_livro(isbn)

                print()
                print(livro)

            elif opcao == "3":
                isbn = input("ISBN: ")

                disponivel = biblioteca.verificar_disponibilidade(
                    isbn
                )

                if disponivel:
                    print("Livro disponível para empréstimo.")
                else:
                    print("Livro indisponível.")

            elif opcao == "4":
                isbn = input("ISBN: ")

                livro = biblioteca.emprestar_livro(isbn)

                print("Empréstimo realizado com sucesso.")
                print(
                    f"Exemplares restantes: "
                    f"{livro.quantidade_disponivel}"
                )

            elif opcao == "5":
                isbn = input("ISBN: ")

                livro = biblioteca.devolver_livro(isbn)

                print("Devolução realizada com sucesso.")
                print(
                    f"Exemplares disponíveis: "
                    f"{livro.quantidade_disponivel}"
                )

            elif opcao == "6":
                livros = biblioteca.listar_livros()

                if not livros:
                    print("Nenhum livro cadastrado.")

                for livro in livros:
                    print("\n----------------------")
                    print(livro)

            elif opcao == "0":
                print("Sistema encerrado.")
                break

            else:
                print("Opção inválida.")

        except ValueError as erro:
            print(f"\nErro: {erro}")

        except Exception as erro:
            print(f"\nErro inesperado: {erro}")


if __name__ == "__main__":
    main()