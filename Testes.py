from criptolib import InteiroModular, Matriz, Congruencias


def obter_inteiro(mensagem: str) -> int:
    """Função auxiliar para garantir que o usuário digite um número inteiro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("[ERRO DE DIGITAÇÃO] Por favor, digite um número inteiro válido.")


def obter_matriz(ordem: int) -> list[list[int]]:
    """Função auxiliar para ler uma matriz quadrada do usuário."""
    matriz = []
    print(
        f"\nDigite os elementos da matriz {ordem}x{ordem} (linha por linha, separados por espaço):"
    )
    for i in range(ordem):
        while True:
            try:
                linha = input(f"Linha {i+1}: ").strip().split()
                linha_ints = [int(x) for x in linha]
                if len(linha_ints) != ordem:
                    print(
                        f"[ERRO DE DIGITAÇÃO] Você deve digitar exatamente {ordem} números separados por espaço."
                    )
                    continue
                matriz.append(linha_ints)
                break
            except ValueError:
                print("[ERRO DE DIGITAÇÃO] Por favor, digite apenas números inteiros.")
    return matriz


def menu_aritmetica_modular():
    while True:
        print("\n" + "=" * 30)
        print("=== SUB-MENU: ARITMÉTICA MODULAR ===")
        print("1. Adição (a + b mod n)")
        print("2. Subtração (a - b mod n)")
        print("3. Multiplicação (a * b mod n)")
        print("4. Divisão Modular (a / b mod n)")
        print("5. Potenciação (a^b mod n)")
        print("6. Inverso Modular (a^-1 mod n)")
        print("0. Voltar ao Menu Principal")
        print("=" * 30)

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break

        if opcao in ["1", "2", "3", "4", "5"]:
            a = obter_inteiro("Digite o valor de a: ")
            b = obter_inteiro("Digite o valor de b: ")
            n = obter_inteiro("Digite o valor do módulo n: ")

            try:
                elem_a = InteiroModular(a, n)
                if opcao == "1":
                    print(f"\nResultado: {elem_a.adicao(b)}")
                elif opcao == "2":
                    print(f"\nResultado: {elem_a.subtracao(b)}")
                elif opcao == "3":
                    print(f"\nResultado: {elem_a.multiplicacao(b)}")
                elif opcao == "4":
                    print(f"\nResultado: {elem_a.divisao_modular(b)}")
                elif opcao == "5":
                    print(f"\nResultado: {elem_a.exponenciacao(b)}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "6":
            a = obter_inteiro("Digite o valor de a: ")
            n = obter_inteiro("Digite o valor do módulo n: ")
            try:
                elem_a = InteiroModular(a, n)
                print(f"\nResultado: {elem_a.inverso_modular()}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")
        else:
            print("\nOpção inválida. Tente novamente.")


def menu_principal():
    while True:
        print("\n" + "=" * 30)
        print("=== MENU PRINCIPAL: CRIPTOLIB ===")
        print("1. Aritmética Modular (Sub-menu)")
        print("2. Verificar Número Primo")
        print("3. MDC")
        print("4. Euclides Estendido")
        print("5. Função Phi de Euler")
        print("6. Teorema Chinês do Resto")
        print("7. Determinante de Matriz")
        print("8. Inversa de Matriz")
        print("9. Inversa Modular da Matriz")
        print("0. Sair")
        print("=" * 30)

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("\nEncerrando o programa...")
            break

        elif opcao == "1":
            menu_aritmetica_modular()

        elif opcao == "2":
            num = obter_inteiro("Digite o número para verificar: ")
            try:
                resultado = InteiroModular.e_primo(num)
                print(f"\nO número {num} é primo? {resultado}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao in ["3", "4"]:
            a = obter_inteiro("Digite o valor de a: ")
            b = obter_inteiro("Digite o valor de b: ")
            try:
                if opcao == "3":
                    print(f"\nMDC({a}, {b}): {InteiroModular.mdc(a, b)}")
                elif opcao == "4":
                    mdc, x, y = InteiroModular.euclides_estendido(a, b)
                    print(f"\nResultado -> MDC: {mdc} | x: {x} | y: {y}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "5":
            n = obter_inteiro("Digite o valor de n para calcular ϕ(n): ")
            try:
                print(f"\nϕ({n}) = {InteiroModular.phi_de_euler(n)}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "6":
            try:
                qtd = obter_inteiro("Quantas congruências tem o sistema? ")
                if qtd <= 0:
                    print("\n[ERRO] O número de congruências deve ser positivo.")
                    continue

                residuos = []
                modulos = []

                print("\nInsira os valores no formato (x ≡ resíduo mod módulo):")
                for i in range(qtd):
                    res = obter_inteiro(f"Resíduo {i+1}: ")
                    mod = obter_inteiro(f"Módulo {i+1}: ")
                    residuos.append(res)
                    modulos.append(mod)

                sistema = Congruencias(residuos, modulos)
                resultado = sistema.resolver()
                print(f"\nResultado: x = {resultado}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao in ["7", "8", "9"]:
            ordem = obter_inteiro(
                "Digite a ordem da matriz quadrada (ex: 3 para 3x3): "
            )
            if ordem <= 0:
                print("\n[ERRO] A ordem da matriz deve ser um número positivo.")
                continue

            dados_matriz = obter_matriz(ordem)

            try:
                matriz = Matriz(dados_matriz)
                if opcao == "7":
                    resultado = matriz.determinante()
                    print(f"\nO determinante da matriz é: {resultado}")
                elif opcao == "8":
                    matriz_inversa = matriz.inversa()
                    print(f"\nA matriz inversa é:\n{matriz_inversa.dados}")
                elif opcao == "9":
                    n = obter_inteiro("Digite o valor do módulo n: ")
                    matriz_inversa_mod = matriz.inversa_modular(n)
                    print(
                        f"\nA matriz inversa no módulo {n} é:\n{matriz_inversa_mod.dados}"
                    )
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()