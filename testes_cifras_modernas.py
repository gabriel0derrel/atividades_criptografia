import unittest

from criptolib.cifras.modernas import SDES, DES, AES, RC5


def _bits_hexadecimal(valor: str) -> str:
    return f"{int(valor, 16):0{len(valor) * 4}b}"


class TestesAES(unittest.TestCase):
    def test_vetor_conhecido_aes_128(self):
        chave = AES(_bits_hexadecimal("000102030405060708090A0B0C0D0E0F"))
        texto = _bits_hexadecimal("00112233445566778899AABBCCDDEEFF")
        cifra_esperada = _bits_hexadecimal("69C4E0D86A7B0430D8CDB78070B4C55A")

        self.assertEqual(chave.cifrar_bits(texto), cifra_esperada)
        self.assertEqual(chave.decifrar_bits(cifra_esperada), texto)

    def test_vetor_conhecido_aes_192(self):
        chave = AES(
            _bits_hexadecimal(
                "000102030405060708090A0B0C0D0E0F1011121314151617"
            )
        )
        texto = _bits_hexadecimal("00112233445566778899AABBCCDDEEFF")
        cifra_esperada = _bits_hexadecimal("DDA97CA4864CDFE06EAF70A0EC0D7191")

        self.assertEqual(chave.cifrar_bits(texto), cifra_esperada)
        self.assertEqual(chave.decifrar_bits(cifra_esperada), texto)

    def test_vetor_conhecido_aes_256(self):
        chave = AES(
            _bits_hexadecimal(
                "000102030405060708090A0B0C0D0E0F"
                "101112131415161718191A1B1C1D1E1F"
            )
        )
        texto = _bits_hexadecimal("00112233445566778899AABBCCDDEEFF")
        cifra_esperada = _bits_hexadecimal("8EA2B7CA516745BFEAFC49904B496089")

        self.assertEqual(chave.cifrar_bits(texto), cifra_esperada)
        self.assertEqual(chave.decifrar_bits(cifra_esperada), texto)

    def test_compatibilidade_dos_metodos_cifrar_e_decifrar(self):
        chave = AES("0" * 128)
        texto = "0" * 128

        cifra = chave.cifrar(texto)

        self.assertEqual(cifra, chave.cifrar_bits(texto))
        self.assertEqual(chave.decifrar(cifra), texto)

    def test_cifra_e_decifra_texto_utf8(self):
        chave = AES("0" * 128)

        for texto in ("", "SecureDocs", "São João: ação e informação."):
            with self.subTest(texto=texto):
                pacote = chave.cifrar_texto(texto)
                self.assertEqual(chave.decifrar_texto(pacote), texto)


def menu_cifras():
    while True:
        print("\n" + "=" * 30)
        print("=== MENU PRINCIPAL: CIFRAS ===")
        print("1. Cifra S-DES")
        print("2. Cifra DES")
        print("3. Cifra AES")
        print("4. Cifra RC5")
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
                cifra = SDES(chave)

                acao = input("Deseja (1) Cifrar ou (2) Decifrar? ").strip()
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

        elif opcao == "2":
            print("\n--- Cifra DES ---")
            chave = input("Digite a chave binária (64 bits): ").strip()

            try:
                cifra = DES(chave)

                print("\nSelecione o modo de operação:")
                print("1. Cifrar bits (binário)")
                print("2. Decifrar bits (binário)")
                print("3. Cifrar texto (modo CBC com IV)")
                print("4. Decifrar texto (modo CBC com IV)")
                modo = input("Opção: ").strip()

                if modo == "1":
                    texto = input("Digite a mensagem binária (múltiplo de 64 bits): ").strip()
                    print(f"\nResultado: {cifra.cifrar_bits(texto)}")
                elif modo == "2":
                    texto = input("Digite a cifra binária (múltiplo de 64 bits): ").strip()
                    print(f"\nResultado: {cifra.decifrar_bits(texto)}")
                elif modo == "3":
                    texto = input("Digite o texto legível: ")
                    print(f"\nResultado (Hex): {cifra.cifrar_texto(texto)}")
                elif modo == "4":
                    pacote_hex = input("Digite o pacote hexadecimal: ").strip()
                    print(f"\nResultado: {cifra.decifrar_texto(pacote_hex)}")
                else:
                    print("\n[ERRO] Opção de modo inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "3":
            print("\n--- Cifra AES ---")
            chave = input("Digite a chave binária (128, 192 ou 256 bits): ").strip()

            try:
                cifra = AES(chave)

                print("\nSelecione o modo de operação:")
                print("1. Cifrar bits (binário)")
                print("2. Decifrar bits (binário)")
                print("3. Cifrar texto (modo CBC com IV)")
                print("4. Decifrar texto (modo CBC com IV)")
                modo = input("Opção: ").strip()

                if modo == "1":
                    texto = input("Digite a mensagem binária (múltiplo de 128 bits): ").strip()
                    print(f"\nResultado: {cifra.cifrar_bits(texto)}")
                elif modo == "2":
                    texto = input("Digite a cifra binária (múltiplo de 128 bits): ").strip()
                    print(f"\nResultado: {cifra.decifrar_bits(texto)}")
                elif modo == "3":
                    texto = input("Digite o texto legível: ")
                    print(f"\nResultado (Hex): {cifra.cifrar_texto(texto)}")
                elif modo == "4":
                    pacote_hex = input("Digite o pacote hexadecimal: ").strip()
                    print(f"\nResultado: {cifra.decifrar_texto(pacote_hex)}")
                else:
                    print("\n[ERRO] Opção de modo inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        elif opcao == "4":
            print("\n--- Cifra RC5 ---")
            chave = input("Digite a chave binária (múltiplo de 8 bits): ").strip()

            try:
                cifra = RC5(chave)

                print("\nParâmetros: RC5-32/12 (blocos de 64 bits).")
                acao = input("Deseja (1) Cifrar ou (2) Decifrar? ").strip()
                if acao == "1":
                    texto = input(
                        "Digite a mensagem binária (múltiplo de 64 bits): "
                    ).strip()
                    print(f"\nResultado: {cifra.cifrar_bits(texto)}")
                elif acao == "2":
                    texto = input(
                        "Digite a cifra binária (múltiplo de 64 bits): "
                    ).strip()
                    print(f"\nResultado: {cifra.decifrar_bits(texto)}")
                else:
                    print("\n[ERRO] Ação inválida.")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_cifras()
