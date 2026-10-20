from criptolib.cifras.modernas.sdes import Sdes


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
        print("1. Cifra S-DES")
        print("0. Sair")
        print("=" * 30)

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("\nEncerrando o programa...")
            break

        elif opcao == "1":
            print("\n--- Cifra S-DES ---")
            chave = input("Digite a chave (10 bits): ").strip()
            
            try:
                cifra = Sdes(chave)

                acao = input("Deseja (1) Cifrar ou (2) Decifrar? ")
                if acao == "1":
                    texto = input(
                        "Digite a mensagem binária para cifrar "
                        "(0 ou 1, em blocos de 8 bits): "
                    ).strip()
                    print(f"\nResultado: {cifra.cifrar(texto)}")
                elif acao == "2":
                    texto = input(
                        "Digite a cifra binária para decifrar "
                        "(0 ou 1, em blocos de 8 bits): "
                    ).strip()
                    print(f"\nResultado: {cifra.decifrar(texto)}")
                else:
                    print("\n[ERRO] Ação inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_cifras()
