import secrets
import string
from pathlib import Path


class AES:
    """Cifra de bloco AES (FIPS-197) com chaves de 128, 192 ou 256 bits.

    O estado é uma lista de 16 bytes em ordem de colunas: o byte da linha
    ``l`` e coluna ``c`` fica no índice ``4 * c + l``. A implementação é
    didática e não deve ser usada para proteger documentos reais.
    """

    _TAMANHO_BLOCO = 16
    _TAMANHOS_CHAVE = (128, 192, 256)
    _ASSINATURA_ARQUIVO = b"SECUREDOCS-AES-CBC\x01"
    _POLINOMIO = 0x11B
    _S_BOX = (
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
    )
    _S_BOX_INV = (
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
    )
    _RCON = (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36)
    _MIX_COLUNAS = (
        (2, 3, 1, 1),
        (1, 2, 3, 1),
        (1, 1, 2, 3),
        (3, 1, 1, 2),
    )
    _MIX_COLUNAS_INV = (
        (14, 11, 13, 9),
        (9, 14, 11, 13),
        (13, 9, 14, 11),
        (11, 13, 9, 14),
    )

    def __init__(self, chave: str):
        self._validar_chave(chave)
        self._subchaves = self._expandir_chave(
            int(chave, 2).to_bytes(len(chave) // 8, "big")
        )

    @classmethod
    def _validar_chave(cls, chave: str) -> None:
        if not isinstance(chave, str):
            raise TypeError("A chave deve ser uma string binária.")
        if len(chave) not in cls._TAMANHOS_CHAVE or any(
            bit not in "01" for bit in chave
        ):
            raise ValueError(
                "A chave deve conter exatamente 128, 192 ou 256 bits (0 ou 1)."
            )

    @classmethod
    def _expandir_chave(cls, chave: bytes) -> tuple[tuple[int, ...], ...]:
        nk = len(chave) // 4
        rodadas = nk + 6
        palavras = [list(chave[4 * i:4 * i + 4]) for i in range(nk)]

        for i in range(nk, 4 * (rodadas + 1)):
            temporario = palavras[i - 1][:]
            if i % nk == 0:
                temporario = temporario[1:] + temporario[:1]
                temporario = [cls._S_BOX[byte] for byte in temporario]
                temporario[0] ^= cls._RCON[i // nk - 1]
            elif nk > 6 and i % nk == 4:
                temporario = [cls._S_BOX[byte] for byte in temporario]
            palavras.append([a ^ b for a, b in zip(palavras[i - nk], temporario)])

        return tuple(
            tuple(byte for palavra in palavras[4 * r:4 * r + 4] for byte in palavra)
            for r in range(rodadas + 1)
        )

    @classmethod
    def _multiplicar(cls, a: int, b: int) -> int:
        resultado = 0
        while b:
            if b & 1:
                resultado ^= a
            a <<= 1
            if a & 0x100:
                a ^= cls._POLINOMIO
            b >>= 1
        return resultado

    @staticmethod
    def _adicionar_chave(estado: list[int], subchave: tuple[int, ...]) -> list[int]:
        return [a ^ b for a, b in zip(estado, subchave)]

    @staticmethod
    def _substituir_bytes(estado: list[int], caixa: tuple[int, ...]) -> list[int]:
        return [caixa[byte] for byte in estado]

    @staticmethod
    def _deslocar_linhas(estado: list[int]) -> list[int]:
        return [estado[4 * ((c + l) % 4) + l] for c in range(4) for l in range(4)]

    @staticmethod
    def _deslocar_linhas_inv(estado: list[int]) -> list[int]:
        return [estado[4 * ((c - l) % 4) + l] for c in range(4) for l in range(4)]

    @classmethod
    def _misturar_colunas(
        cls, estado: list[int], matriz: tuple[tuple[int, ...], ...]
    ) -> list[int]:
        resultado = []
        for inicio in range(0, 16, 4):
            coluna = estado[inicio:inicio + 4]
            for linha in matriz:
                valor = 0
                for fator, byte in zip(linha, coluna):
                    valor ^= cls._multiplicar(byte, fator)
                resultado.append(valor)
        return resultado

    def _cifrar_bloco(self, bloco: bytes) -> bytes:
        estado = self._adicionar_chave(list(bloco), self._subchaves[0])

        for subchave in self._subchaves[1:-1]:
            estado = self._substituir_bytes(estado, self._S_BOX)
            estado = self._deslocar_linhas(estado)
            estado = self._misturar_colunas(estado, self._MIX_COLUNAS)
            estado = self._adicionar_chave(estado, subchave)

        estado = self._substituir_bytes(estado, self._S_BOX)
        estado = self._deslocar_linhas(estado)
        estado = self._adicionar_chave(estado, self._subchaves[-1])
        return bytes(estado)

    def _decifrar_bloco(self, bloco: bytes) -> bytes:
        estado = self._adicionar_chave(list(bloco), self._subchaves[-1])

        for subchave in reversed(self._subchaves[1:-1]):
            estado = self._deslocar_linhas_inv(estado)
            estado = self._substituir_bytes(estado, self._S_BOX_INV)
            estado = self._adicionar_chave(estado, subchave)
            estado = self._misturar_colunas(estado, self._MIX_COLUNAS_INV)

        estado = self._deslocar_linhas_inv(estado)
        estado = self._substituir_bytes(estado, self._S_BOX_INV)
        estado = self._adicionar_chave(estado, self._subchaves[0])
        return bytes(estado)

    def _processar(self, mensagem: str, operacao) -> str:
        if not isinstance(mensagem, str):
            raise TypeError("A mensagem deve ser uma string binária.")
        if (
            not mensagem
            or len(mensagem) % 128 != 0
            or any(bit not in "01" for bit in mensagem)
        ):
            raise ValueError(
                "A mensagem deve conter blocos completos de 128 bits (0 ou 1)."
            )

        resultado = []
        for inicio in range(0, len(mensagem), 128):
            bloco = int(mensagem[inicio:inicio + 128], 2).to_bytes(16, "big")
            processado = operacao(bloco)
            resultado.append(f"{int.from_bytes(processado, 'big'):0128b}")
        return "".join(resultado)

    def cifrar_bits(self, mensagem: str) -> str:
        return self._processar(mensagem, self._cifrar_bloco)

    def decifrar_bits(self, cifra: str) -> str:
        return self._processar(cifra, self._decifrar_bloco)

    def cifrar(self, mensagem: str) -> str:
        return self.cifrar_bits(mensagem)

    def decifrar(self, cifra: str) -> str:
        return self.decifrar_bits(cifra)

    @staticmethod
    def _validar_caminhos_arquivo(
        arquivo_entrada: str | Path,
        arquivo_saida: str | Path,
    ) -> tuple[Path, Path]:
        entrada = Path(arquivo_entrada)
        saida = Path(arquivo_saida)
        if entrada.resolve() == saida.resolve():
            raise ValueError("Os caminhos de entrada e saída devem ser diferentes.")
        return entrada, saida

    def cifrar_arquivo(
        self,
        arquivo_entrada: str | Path,
        arquivo_saida: str | Path,
    ) -> None:
        entrada, saida = self._validar_caminhos_arquivo(
            arquivo_entrada,
            arquivo_saida,
        )
        dados = entrada.read_bytes()
        quantidade_padding = self._TAMANHO_BLOCO - (
            len(dados) % self._TAMANHO_BLOCO
        )
        dados += bytes([quantidade_padding]) * quantidade_padding

        iv = secrets.token_bytes(self._TAMANHO_BLOCO)
        anterior = iv
        cifra = bytearray()

        for inicio in range(0, len(dados), self._TAMANHO_BLOCO):
            bloco = dados[inicio:inicio + self._TAMANHO_BLOCO]
            combinado = bytes(a ^ b for a, b in zip(bloco, anterior))
            bloco_cifrado = self._cifrar_bloco(combinado)
            cifra.extend(bloco_cifrado)
            anterior = bloco_cifrado

        saida.write_bytes(self._ASSINATURA_ARQUIVO + iv + cifra)

    def decifrar_arquivo(
        self,
        arquivo_entrada: str | Path,
        arquivo_saida: str | Path,
    ) -> None:
        entrada, saida = self._validar_caminhos_arquivo(
            arquivo_entrada,
            arquivo_saida,
        )
        pacote = entrada.read_bytes()
        tamanho_assinatura = len(self._ASSINATURA_ARQUIVO)
        if not pacote.startswith(self._ASSINATURA_ARQUIVO):
            raise ValueError(
                "O arquivo selecionado não foi cifrado pela demonstração AES."
            )

        dados_cifrados = pacote[tamanho_assinatura:]
        if len(dados_cifrados) < 2 * self._TAMANHO_BLOCO or (
            len(dados_cifrados) % self._TAMANHO_BLOCO != 0
        ):
            raise ValueError(
                "O arquivo cifrado deve conter um IV e ao menos "
                "um bloco cifrado AES."
            )

        iv = dados_cifrados[:self._TAMANHO_BLOCO]
        anterior = iv
        dados = bytearray()

        for inicio in range(
            self._TAMANHO_BLOCO,
            len(dados_cifrados),
            self._TAMANHO_BLOCO,
        ):
            bloco_cifrado = dados_cifrados[
                inicio:inicio + self._TAMANHO_BLOCO
            ]
            bloco_decifrado = self._decifrar_bloco(bloco_cifrado)
            dados.extend(a ^ b for a, b in zip(bloco_decifrado, anterior))
            anterior = bloco_cifrado

        quantidade_padding = dados[-1]
        if (
            not 1 <= quantidade_padding <= self._TAMANHO_BLOCO
            or dados[-quantidade_padding:]
            != bytes([quantidade_padding]) * quantidade_padding
        ):
            raise ValueError(
                "Preenchimento inválido; verifique a chave ou o arquivo cifrado."
            )

        saida.write_bytes(dados[:-quantidade_padding])

    def cifrar_texto(self, texto: str) -> str:
        if not isinstance(texto, str):
            raise TypeError("O texto deve ser uma string.")

        dados = texto.encode("utf-8")
        quantidade_padding = 16 - len(dados) % 16
        dados += bytes([quantidade_padding]) * quantidade_padding

        iv = secrets.token_bytes(16)
        anterior = iv
        saida = bytearray()

        for inicio in range(0, len(dados), 16):
            bloco = dados[inicio:inicio + 16]
            combinado = bytes(a ^ b for a, b in zip(bloco, anterior))
            bloco_cifrado = self._cifrar_bloco(combinado)
            saida.extend(bloco_cifrado)
            anterior = bloco_cifrado

        return (iv + saida).hex()

    def decifrar_texto(self, pacote_hex: str) -> str:
        if not isinstance(pacote_hex, str):
            raise TypeError("O pacote cifrado deve ser uma string hexadecimal.")
        if any(caractere not in string.hexdigits for caractere in pacote_hex):
            raise ValueError("O pacote deve conter somente caracteres hexadecimais.")
        if len(pacote_hex) % 2 != 0:
            raise ValueError("O pacote hexadecimal deve conter pares de caracteres.")

        pacote = bytes.fromhex(pacote_hex)
        if len(pacote) < 32 or len(pacote) % 16 != 0:
            raise ValueError(
                "O pacote deve conter 16 bytes de IV e pelo menos "
                "um bloco cifrado de 16 bytes."
            )

        iv = pacote[:16]
        anterior = iv
        dados = bytearray()

        for inicio in range(16, len(pacote), 16):
            bloco_cifrado = pacote[inicio:inicio + 16]
            bloco_decifrado = self._decifrar_bloco(bloco_cifrado)
            dados.extend(a ^ b for a, b in zip(bloco_decifrado, anterior))
            anterior = bloco_cifrado

        quantidade_padding = dados[-1]
        if (
            not 1 <= quantidade_padding <= 16
            or dados[-quantidade_padding:]
            != bytes([quantidade_padding]) * quantidade_padding
        ):
            raise ValueError(
                "Preenchimento inválido; verifique a chave ou o pacote."
            )

        try:
            return bytes(dados[:-quantidade_padding]).decode("utf-8")
        except UnicodeDecodeError as erro:
            raise ValueError(
                "O conteúdo decifrado não é UTF-8 válido; "
                "verifique a chave ou o pacote."
            ) from erro
