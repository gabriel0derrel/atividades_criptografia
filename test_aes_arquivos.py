import tempfile
import unittest
from pathlib import Path

from criptolib.cifras.modernas import AES


class TestesArquivosAES(unittest.TestCase):
    def setUp(self):
        self.cifra = AES("0" * 128)

    def test_cifra_e_recupera_arquivos_binarios(self):
        exemplos = (
            b"",
            b"documento menor que um bloco",
            bytes(range(256)),
            b"\x00\xff\x80conteudo binario\x00" * 20,
            b"A" * 32,
        )

        with tempfile.TemporaryDirectory() as diretorio:
            pasta = Path(diretorio)
            original = pasta / "original.bin"
            cifrado = pasta / "cifrado.aes"
            recuperado = pasta / "recuperado.bin"

            for dados in exemplos:
                with self.subTest(tamanho=len(dados)):
                    original.write_bytes(dados)
                    self.cifra.cifrar_arquivo(original, cifrado)
                    pacote = cifrado.read_bytes()

                    self.assertGreaterEqual(len(pacote), 32)
                    self.assertEqual(len(pacote) % 16, 0)
                    self.assertNotEqual(pacote, dados)

                    self.cifra.decifrar_arquivo(cifrado, recuperado)
                    self.assertEqual(recuperado.read_bytes(), dados)
                    self.assertEqual(original.read_bytes(), dados)

    def test_rejeita_arquivo_cifrado_incompleto_sem_criar_saida(self):
        with tempfile.TemporaryDirectory() as diretorio:
            pasta = Path(diretorio)
            cifrado = pasta / "cifrado.aes"
            recuperado = pasta / "recuperado.bin"
            cifrado.write_bytes(b"\x00" * 31)

            with self.assertRaises(ValueError):
                self.cifra.decifrar_arquivo(cifrado, recuperado)

            self.assertFalse(recuperado.exists())

    def test_nao_sobrescreve_o_arquivo_de_entrada(self):
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "documento.bin"
            conteudo = b"documento original"
            arquivo.write_bytes(conteudo)

            with self.assertRaises(ValueError):
                self.cifra.cifrar_arquivo(arquivo, arquivo)

            self.assertEqual(arquivo.read_bytes(), conteudo)


if __name__ == "__main__":
    unittest.main()
