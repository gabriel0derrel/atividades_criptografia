import secrets
import string


class Des:
    _IP = (
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
    )
    _IP_INV = (
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
    )
    _EXPANSION = (
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1,
    )
    _P = (
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25,
    )
    _PC1 = (
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4,
    )
    _PC2 = (
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32,
    )
    _SHIFTS = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)
    _S_BOXES = (
        (
            (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
            (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
            (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
            (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
        ),
        (
            (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
            (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
            (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
            (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
        ),
        (
            (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
            (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
            (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
            (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
        ),
        (
            (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
            (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
            (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
            (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
        ),
        (
            (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
            (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
            (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
            (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
        ),
        (
            (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
            (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
            (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
            (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
        ),
        (
            (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
            (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
            (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
            (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
        ),
        (
            (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
            (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
            (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
            (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
        ),
    )

    def __init__(self, chave: str):
        self._validar_bits(chave, "A chave", 64)
        chave_reduzida = self._permutar(int(chave, 2), self._PC1, 64)
        esquerda, direita = chave_reduzida >> 28, chave_reduzida & ((1 << 28) - 1)

        subchaves = []
        mascara = (1 << 28) - 1
        for deslocamento in self._SHIFTS:
            esquerda = (
                (esquerda << deslocamento) | (esquerda >> (28 - deslocamento))
            ) & mascara
            direita = (
                (direita << deslocamento) | (direita >> (28 - deslocamento))
            ) & mascara
            subchaves.append(
                self._permutar((esquerda << 28) | direita, self._PC2, 56)
            )
        self._subchaves = tuple(subchaves)

    @staticmethod
    def _validar_bits(valor: str, nome: str, tamanho: int) -> None:
        if not isinstance(valor, str):
            raise TypeError(f"{nome} deve ser uma string binária.")
        if len(valor) != tamanho or any(bit not in "01" for bit in valor):
            raise ValueError(
                f"{nome} deve conter exatamente {tamanho} bits (0 ou 1)."
            )

    @staticmethod
    def _permutar(valor: int, tabela: tuple[int, ...], tamanho_entrada: int) -> int:
        resultado = 0
        for posicao in tabela:
            resultado = (resultado << 1) | ((valor >> (tamanho_entrada - posicao)) & 1)
        return resultado

    @classmethod
    def _funcao_f(cls, metade_direita: int, subchave: int) -> int:
        expandido = cls._permutar(metade_direita, cls._EXPANSION, 32) ^ subchave
        substituido = 0

        for indice, caixa in enumerate(cls._S_BOXES):
            bloco = (expandido >> (42 - 6 * indice)) & 0b111111
            linha = ((bloco & 0b100000) >> 4) | (bloco & 1)
            coluna = (bloco >> 1) & 0b1111
            substituido = (substituido << 4) | caixa[linha][coluna]

        return cls._permutar(substituido, cls._P, 32)

    @classmethod
    def _processar_bloco(cls, bloco: int, subchaves: tuple[int, ...]) -> int:
        bloco = cls._permutar(bloco, cls._IP, 64)
        esquerda, direita = bloco >> 32, bloco & 0xFFFFFFFF

        for subchave in subchaves:
            esquerda, direita = direita, esquerda ^ cls._funcao_f(direita, subchave)

        return cls._permutar((direita << 32) | esquerda, cls._IP_INV, 64)

    def _processar(self, mensagem: str, subchaves: tuple[int, ...]) -> str:
        if not isinstance(mensagem, str):
            raise TypeError("A mensagem deve ser uma string binária.")
        if len(mensagem) % 64 != 0 or any(bit not in "01" for bit in mensagem):
            raise ValueError(
                "A mensagem deve conter blocos completos de 64 bits (0 ou 1)."
            )

        resultado = []
        for inicio in range(0, len(mensagem), 64):
            bloco = int(mensagem[inicio:inicio + 64], 2)
            cifrado = self._processar_bloco(bloco, subchaves)
            resultado.append(f"{cifrado:064b}")
        return "".join(resultado)

    def cifrar_bits(self, mensagem: str) -> str:
        return self._processar(mensagem, self._subchaves)

    def decifrar_bits(self, cifra: str) -> str:
        return self._processar(cifra, tuple(reversed(self._subchaves)))

    def cifrar(self, mensagem: str) -> str:
        return self.cifrar_bits(mensagem)

    def decifrar(self, cifra: str) -> str:
        return self.decifrar_bits(cifra)

    def cifrar_texto(self, texto: str) -> str:
        if not isinstance(texto, str):
            raise TypeError("O texto deve ser uma string.")

        dados = texto.encode("utf-8")
        quantidade_padding = 8 - len(dados) % 8
        dados += bytes([quantidade_padding]) * quantidade_padding

        iv = secrets.token_bytes(8)
        anterior = iv
        saida = bytearray()

        for inicio in range(0, len(dados), 8):
            bloco = dados[inicio:inicio + 8]
            combinado = bytes(a ^ b for a, b in zip(bloco, anterior))
            valor = self._processar_bloco(
                int.from_bytes(combinado, "big"),
                self._subchaves,
            )
            bloco_cifrado = valor.to_bytes(8, "big")
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
        if len(pacote) < 16 or len(pacote) % 8 != 0:
            raise ValueError(
                "O pacote deve conter 8 bytes de IV e pelo menos "
                "um bloco cifrado de 8 bytes."
            )

        iv = pacote[:8]
        anterior = iv
        dados = bytearray()
        subchaves = tuple(reversed(self._subchaves))

        for inicio in range(8, len(pacote), 8):
            bloco_cifrado = pacote[inicio:inicio + 8]
            valor = self._processar_bloco(
                int.from_bytes(bloco_cifrado, "big"),
                subchaves,
            )
            bloco_decifrado = valor.to_bytes(8, "big")
            dados.extend(a ^ b for a, b in zip(bloco_decifrado, anterior))
            anterior = bloco_cifrado

        quantidade_padding = dados[-1]
        if (
            not 1 <= quantidade_padding <= 8
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
