from criptolib.cifras.classicas import Cesar, Afim, Hill, AutoChave, Fluxo


def obter_inteiro(mensagem: str) -> int:
    """Função auxiliar para garantir que o usuário digite um número inteiro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("[ERRO DE DIGITAÇÃO] Por favor, digite um número inteiro válido.")


def obter_matriz(ordem: int) -> list[list[int]]:
    """Função auxiliar para ler uma matriz quadrada do usuário para a chave da Cifra de Hill."""
    matriz = []
    print(
        f"\nDigite os elementos da matriz chave {ordem}x{ordem} (linha por linha, separados por espaço):"
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


def menu_cifras():
    while True:
        print("\n" + "=" * 30)
        print("=== MENU PRINCIPAL: CIFRAS ===")
        print("1. Cifra de César")
        print("2. Cifra Afim")
        print("3. Cifra de Hill")
        print("4. Cifra de Autochave")
        print("5. Cifra de Fluxo")
        print("0. Sair")
        print("=" * 30)

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("\nEncerrando o programa...")
            break

        elif opcao == "1":
            print("\n--- Cifra de César ---")
            chave = obter_inteiro("Digite o valor da chave (deslocamento): ")
            
            try:
                cifra = Cesar(chave)
                
                acao = input("Deseja (1) Cifrar ou (2) Decifrar? ")
                if acao == "1":
                    texto = input("Digite a mensagem para cifrar: ")
                    print(f"\nResultado: {cifra.cifrar(texto)}")
                elif acao == "2":
                    texto = input("Digite a mensagem para decifrar: ")
                    print(f"\nResultado: {cifra.decifrar(texto)}")
                else:
                    print("\n[ERRO] Ação inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "2":
            print("\n--- Cifra Afim ---")
            chave_a = obter_inteiro("Digite o valor da chave 'a' (multiplicativa): ")
            chave_b = obter_inteiro("Digite o valor da chave 'b' (aditiva): ")
            
            try:
                cifra = Afim(chave_a, chave_b)
                
                acao = input("Deseja (1) Cifrar ou (2) Decifrar? ")
                if acao == "1":
                    texto = input("Digite a mensagem para cifrar: ")
                    print(f"\nResultado: {cifra.cifrar(texto)}")
                elif acao == "2":
                    texto = input("Digite a mensagem para decifrar: ")
                    print(f"\nResultado: {cifra.decifrar(texto)}")
                else:
                    print("\n[ERRO] Ação inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "3":
            print("\n--- Cifra de Hill ---")
            ordem = obter_inteiro("Digite a ordem da matriz chave quadrada (ex: 2 para 2x2, 3 para 3x3): ")
            
            if ordem <= 0:
                print("\n[ERRO] A ordem da matriz deve ser um número positivo.")
                continue

            chave_matriz = obter_matriz(ordem)

            try:
                cifra = Hill(chave_matriz)
                
                acao = input("Deseja (1) Cifrar ou (2) Decifrar? ")
                if acao == "1":
                    texto = input("Digite a mensagem para cifrar: ")
                    print(f"\nResultado: {cifra.cifrar(texto)}")
                elif acao == "2":
                    texto = input("Digite a mensagem para decifrar: ")
                    print(f"\nResultado: {cifra.decifrar(texto)}")
                else:
                    print("\n[ERRO] Ação inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "4":
            print("\n--- Cifra de Autochave ---")
            chave = input("Digite o caractere ou o inteiro da chave inicial (K0): ").strip()

            try:
                try:
                    chave = int(chave)
                except ValueError:
                    pass

                cifra = AutoChave(chave)

                acao = input("Deseja (1) Cifrar ou (2) Decifrar? ")
                if acao == "1":
                    texto = input("Digite a mensagem para cifrar: ")
                    print(f"\nResultado: {cifra.cifrar(texto)}")
                elif acao == "2":
                    texto = input("Digite a mensagem para decifrar: ")
                    print(f"\nResultado: {cifra.decifrar(texto)}")
                else:
                    print("\n[ERRO] Ação inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "5":
            print("\n--- Cifra de Fluxo ---")
            seed = obter_inteiro("Digite o valor da semente (seed) para o gerador de números aleatórios: ")

            try:
                cifra = Fluxo(seed)

                acao = input("Deseja (1) Cifrar ou (2) Decifrar? ")
                if acao == "1":
                    texto = input("Digite a mensagem para cifrar: ")
                    print(f"\nResultado: {cifra.cifrar(texto)}")
                elif acao == "2":
                    texto = input("Digite a mensagem para decifrar: ")
                    print(f"\nResultado: {cifra.decifrar(texto)}")
                else:
                    print("\n[ERRO] Ação inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_cifras()
