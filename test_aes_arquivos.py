import tempfile
import unittest
from pathlib import Path

from criptolib.cifras.modernas import AES


class TestesArquivosAES(unittest.TestCase):
    def setUp(self):
        self.cifra = AES("0" * 128)

    def test_cifra_e_recupera_arquivos_binarios(self):
        exemplos = (
            ("vazio.bin", b""),
            ("documento.pdf", b"%PDF-1.7\nconteudo de exemplo"),
            ("relatorio.docx", b"PK\x03\x04" + bytes(range(256))),
            ("planilha.xlsx", b"PK\x03\x04" + b"\x00\xff\x80dados\x00" * 20),
            ("multiplo.bin", b"A" * 32),
        )

        with tempfile.TemporaryDirectory() as diretorio:
            pasta = Path(diretorio)

            for nome, dados in exemplos:
                with self.subTest(tamanho=len(dados)):
                    original = pasta / nome
                    cifrado = pasta / f"{nome}.sdocaes"
                    recuperado = pasta / f"recuperado_{nome}"
                    original.write_bytes(dados)
                    self.cifra.cifrar_arquivo(original, cifrado)
                    pacote = cifrado.read_bytes()

                    self.assertGreaterEqual(len(pacote), 32)
                    self.assertEqual(
                        (len(pacote) - len(AES._ASSINATURA_ARQUIVO)) % 16,
                        0,
                    )
                    self.assertTrue(
                        pacote.startswith(AES._ASSINATURA_ARQUIVO)
                    )
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

    def test_rejeita_arquivo_comum_sem_criar_saida(self):
        with tempfile.TemporaryDirectory() as diretorio:
            pasta = Path(diretorio)
            original = pasta / "documento.pdf"
            recuperado = pasta / "recuperado.pdf"
            original.write_bytes(b"%PDF-1.7 " + b"conteudo" * 10)

            with self.assertRaisesRegex(ValueError, "não foi cifrado"):
                self.cifra.decifrar_arquivo(original, recuperado)

            self.assertFalse(recuperado.exists())

    def test_permite_cifrar_um_arquivo_cifrado_novamente(self):
        with tempfile.TemporaryDirectory() as diretorio:
            pasta = Path(diretorio)
            original = pasta / "original.pdf"
            primeira_cifra = pasta / "original.pdf.sdocaes"
            segunda_cifra = pasta / "segunda.sdocaes"
            primeira_recuperacao = pasta / "primeira_recuperacao.pdf"
            segunda_recuperacao = pasta / "segunda_recuperacao.sdocaes"
            dados = b"%PDF-1.7 conteudo binario"
            original.write_bytes(dados)

            self.cifra.cifrar_arquivo(original, primeira_cifra)
            primeira_cifra_bytes = primeira_cifra.read_bytes()
            self.cifra.cifrar_arquivo(primeira_cifra, segunda_cifra)
            self.cifra.decifrar_arquivo(segunda_cifra, primeira_recuperacao)
            self.cifra.decifrar_arquivo(primeira_recuperacao, segunda_recuperacao)

            self.assertEqual(primeira_recuperacao.read_bytes(), primeira_cifra_bytes)
            self.assertEqual(segunda_recuperacao.read_bytes(), dados)

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
