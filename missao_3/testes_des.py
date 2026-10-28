import unittest

from criptolib.cifras.modernas import Des


def _bits_hexadecimal(valor: str) -> str:
    return f"{int(valor, 16):0{len(valor) * 4}b}"


class TestesDes(unittest.TestCase):
    def setUp(self):
        self.chave = Des(_bits_hexadecimal("133457799BBCDFF1"))
        self.texto = _bits_hexadecimal("0123456789ABCDEF")
        self.cifra = _bits_hexadecimal("85E813540F0AB405")

    def test_vetor_conhecido_cifra(self):
        self.assertEqual(self.chave.cifrar_bits(self.texto), self.cifra)

    def test_vetor_conhecido_decifra(self):
        self.assertEqual(self.chave.decifrar_bits(self.cifra), self.texto)

    def test_processa_multiplos_blocos(self):
        texto = self.texto * 2
        cifra = self.chave.cifrar_bits(texto)
        self.assertEqual(len(cifra), len(texto))
        self.assertEqual(self.chave.decifrar_bits(cifra), texto)

    def test_mantem_compatibilidade_com_cifrar_e_decifrar(self):
        cifra = self.chave.cifrar(self.texto)
        self.assertEqual(cifra, self.cifra)
        self.assertEqual(self.chave.decifrar(cifra), self.texto)

    def test_aceita_mensagem_vazia(self):
        self.assertEqual(self.chave.cifrar_bits(""), "")
        self.assertEqual(self.chave.decifrar_bits(""), "")

    def test_cifra_e_decifra_texto_utf8(self):
        exemplos = (
            "Oi",
            "",
            "Criptografia aplicada!",
            "São João: ação, coração e informação.",
            "A" * 1000,
        )

        for texto in exemplos:
            with self.subTest(texto=texto[:20]):
                pacote = self.chave.cifrar_texto(texto)
                self.assertEqual(self.chave.decifrar_texto(pacote), texto)
                self.assertEqual(len(pacote) % 16, 0)

    def test_rejeita_texto_com_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self.chave.cifrar_texto(123)

    def test_rejeita_pacote_hexadecimal_com_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self.chave.decifrar_texto(123)

    def test_rejeita_pacote_com_caracteres_nao_hexadecimais(self):
        with self.assertRaises(ValueError):
            self.chave.decifrar_texto("00 11")

    def test_rejeita_pacote_hexadecimal_com_tamanho_impar(self):
        with self.assertRaises(ValueError):
            self.chave.decifrar_texto("0")

    def test_rejeita_pacote_curto(self):
        with self.assertRaises(ValueError):
            self.chave.decifrar_texto("00" * 8)

    def test_rejeita_pacote_com_padding_invalido(self):
        pacote = bytearray.fromhex(self.chave.cifrar_texto("A"))
        pacote[7] ^= 1

        with self.assertRaisesRegex(ValueError, "Preenchimento inválido"):
            self.chave.decifrar_texto(pacote.hex())

    def test_rejeita_chave_com_tipo_invalido(self):
        with self.assertRaises(TypeError):
            Des(123)

    def test_rejeita_chave_com_tamanho_ou_caracteres_invalidos(self):
        with self.assertRaises(ValueError):
            Des("0" * 63)
        with self.assertRaises(ValueError):
            Des("0" * 63 + "x")

    def test_rejeita_mensagem_com_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self.chave.cifrar_bits(123)

    def test_rejeita_mensagem_sem_blocos_completos(self):
        with self.assertRaises(ValueError):
            self.chave.cifrar_bits("0" * 63)

    def test_rejeita_mensagem_nao_binaria(self):
        with self.assertRaises(ValueError):
            self.chave.decifrar_bits("0" * 63 + "x")


if __name__ == "__main__":
    unittest.main()
