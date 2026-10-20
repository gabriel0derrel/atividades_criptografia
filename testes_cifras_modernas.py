from criptolib.cifras.modernas.sdes import Sdes

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
