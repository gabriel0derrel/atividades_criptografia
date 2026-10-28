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
        self.assertEqual(self.chave.cifrar(self.texto), self.cifra)

    def test_vetor_conhecido_decifra(self):
        self.assertEqual(self.chave.decifrar(self.cifra), self.texto)

    def test_processa_multiplos_blocos(self):
        texto = self.texto * 2
        cifra = self.chave.cifrar(texto)
        self.assertEqual(len(cifra), len(texto))
        self.assertEqual(self.chave.decifrar(cifra), texto)

    def test_aceita_mensagem_vazia(self):
        self.assertEqual(self.chave.cifrar(""), "")
        self.assertEqual(self.chave.decifrar(""), "")

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
            self.chave.cifrar(123)

    def test_rejeita_mensagem_sem_blocos_completos(self):
        with self.assertRaises(ValueError):
            self.chave.cifrar("0" * 63)

    def test_rejeita_mensagem_nao_binaria(self):
        with self.assertRaises(ValueError):
            self.chave.decifrar("0" * 63 + "x")


if __name__ == "__main__":
    unittest.main()
