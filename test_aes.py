import unittest

from criptolib.cifras.modernas import AES


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


if __name__ == "__main__":
    unittest.main()
