class Sdes:
    _P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
    _P8 = (6, 3, 7, 4, 8, 5, 10, 9)
    _IP = (2, 6, 3, 1, 4, 8, 5, 7)
    _IP_INV = (4, 1, 3, 5, 7, 2, 8, 6)
    _EP = (4, 1, 2, 3, 2, 3, 4, 1)
    _P4 = (2, 4, 3, 1)
    _S0 = (
        (1, 0, 3, 2),
        (3, 2, 1, 0),
        (0, 2, 1, 3),
        (3, 1, 3, 2),
    )
    _S1 = (
        (0, 1, 2, 3),
        (2, 0, 1, 3),
        (3, 0, 1, 0),
        (2, 1, 0, 3),
    )

    def __init__(self, chave: str):
        if not isinstance(chave, str):
            raise TypeError("A chave deve ser uma string binária de 10 bits.")
        if len(chave) != 10 or any(bit not in "01" for bit in chave):
            raise ValueError("A chave deve conter exatamente 10 bits (0 ou 1).")

        self.chave = chave
        chave_p10 = self._permutar(chave, self._P10)
        esquerda, direita = chave_p10[:5], chave_p10[5:]

        esquerda, direita = self._deslocar(esquerda, 1), self._deslocar(direita, 1)
        self._k1 = self._permutar(esquerda + direita, self._P8)

        esquerda, direita = self._deslocar(esquerda, 2), self._deslocar(direita, 2)
        self._k2 = self._permutar(esquerda + direita, self._P8)

    @staticmethod
    def _permutar(bits: str, tabela: tuple[int, ...]) -> str:
        return "".join(bits[posicao - 1] for posicao in tabela)

    @staticmethod
    def _deslocar(bits: str, quantidade: int) -> str:
        return bits[quantidade:] + bits[:quantidade]

    @staticmethod
    def _xor(esquerda: str, direita: str) -> str:
        return "".join("1" if a != b else "0" for a, b in zip(esquerda, direita))

    @classmethod
    def _substituir(cls, bits: str, caixa: tuple[tuple[int, ...], ...]) -> str:
        linha = int(bits[0] + bits[3], 2)
        coluna = int(bits[1:3], 2)
        return f"{caixa[linha][coluna]:02b}"

    @classmethod
    def _funcao_f(cls, metade: str, subchave: str) -> str:
        expandido = cls._permutar(metade, cls._EP)
        resultado_xor = cls._xor(expandido, subchave)
        substituido = cls._substituir(resultado_xor[:4], cls._S0)
        substituido += cls._substituir(resultado_xor[4:], cls._S1)
        return cls._permutar(substituido, cls._P4)

    @classmethod
    def _rodada(cls, bloco: str, subchave: str) -> str:
        esquerda, direita = bloco[:4], bloco[4:]
        return cls._xor(esquerda, cls._funcao_f(direita, subchave)) + direita

    @staticmethod
    def _validar_mensagem(mensagem: str) -> None:
        if not isinstance(mensagem, str):
            raise TypeError("A mensagem deve ser uma string binária.")
        if len(mensagem) % 8 != 0 or any(bit not in "01" for bit in mensagem):
            raise ValueError(
                "A mensagem deve conter blocos completos de 8 bits (0 ou 1)."
            )

    def _processar(self, mensagem: str, primeira: str, segunda: str) -> str:
        self._validar_mensagem(mensagem)
        resultado = []
        for inicio in range(0, len(mensagem), 8):
            bloco = self._permutar(mensagem[inicio : inicio + 8], self._IP)
            bloco = self._rodada(bloco, primeira)
            bloco = bloco[4:] + bloco[:4]
            bloco = self._rodada(bloco, segunda)
            resultado.append(self._permutar(bloco, self._IP_INV))
        return "".join(resultado)

    def cifrar(self, texto: str) -> str:
        return self._processar(texto, self._k1, self._k2)

    def decifrar(self, cifra: str) -> str:
        return self._processar(cifra, self._k2, self._k1)
