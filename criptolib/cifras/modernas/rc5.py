class RC5:
    """RC5 com palavras de 16, 32 ou 64 bits e blocos de duas palavras.

    A chave e as mensagens são strings binárias. Por padrão são usadas palavras
    de 32 bits e 12 rodadas (RC5-32/12), com bloco de 64 bits.
    Implementação didática; não recomendada para proteger dados reais.
    """

    _CONSTANTES = {
        16: (0xB7E1, 0x9E37),
        32: (0xB7E15163, 0x9E3779B9),
        64: (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15),
    }

    def __init__(self, chave: str, rodadas: int = 12, tamanho_palavra: int = 32):
        if not isinstance(chave, str):
            raise TypeError("A chave deve ser uma string binária.")
        if not chave or len(chave) % 8 or any(bit not in "01" for bit in chave):
            raise ValueError("A chave deve conter bytes completos em formato binário.")
        if tamanho_palavra not in self._CONSTANTES:
            raise ValueError("O tamanho da palavra deve ser 16, 32 ou 64 bits.")
        if not isinstance(rodadas, int) or isinstance(rodadas, bool) or rodadas < 0:
            raise ValueError("O número de rodadas deve ser um inteiro não negativo.")

        self.tamanho_palavra = tamanho_palavra
        self.rodadas = rodadas
        self._bits = tamanho_palavra
        self._mascara = (1 << tamanho_palavra) - 1
        self._subchaves = self._expandir_chave(bytes.fromhex(f"{int(chave, 2):0{len(chave) // 4}x}"))

    def _rotacionar_esquerda(self, valor: int, quantidade: int) -> int:
        quantidade %= self._bits
        valor &= self._mascara
        return ((valor << quantidade) | (valor >> (self._bits - quantidade))) & self._mascara

    def _rotacionar_direita(self, valor: int, quantidade: int) -> int:
        quantidade %= self._bits
        valor &= self._mascara
        return ((valor >> quantidade) | (valor << (self._bits - quantidade))) & self._mascara

    def _expandir_chave(self, chave: bytes) -> tuple[int, ...]:
        u = self._bits // 8
        quantidade_palavras = max(1, (len(chave) + u - 1) // u)
        palavras = [0] * quantidade_palavras
        for indice, byte in enumerate(chave):
            palavras[indice // u] |= byte << (8 * (indice % u))

        p, q = self._CONSTANTES[self._bits]
        quantidade_subchaves = 2 * (self.rodadas + 1)
        subchaves = [(p + i * q) & self._mascara for i in range(quantidade_subchaves)]
        a = b = i = j = 0
        for _ in range(3 * max(quantidade_subchaves, quantidade_palavras)):
            a = subchaves[i] = self._rotacionar_esquerda(
                (subchaves[i] + a + b) & self._mascara, 3
            )
            b = palavras[j] = self._rotacionar_esquerda(
                (palavras[j] + a + b) & self._mascara, a + b
            )
            i = (i + 1) % quantidade_subchaves
            j = (j + 1) % quantidade_palavras
        return tuple(subchaves)

    def _cifrar_bloco(self, a: int, b: int) -> tuple[int, int]:
        a = (a + self._subchaves[0]) & self._mascara
        b = (b + self._subchaves[1]) & self._mascara
        for rodada in range(1, self.rodadas + 1):
            a = (self._rotacionar_esquerda(a ^ b, b) + self._subchaves[2 * rodada]) & self._mascara
            b = (self._rotacionar_esquerda(b ^ a, a) + self._subchaves[2 * rodada + 1]) & self._mascara
        return a, b

    def _decifrar_bloco(self, a: int, b: int) -> tuple[int, int]:
        for rodada in range(self.rodadas, 0, -1):
            b = self._rotacionar_direita((b - self._subchaves[2 * rodada + 1]) & self._mascara, a) ^ a
            a = self._rotacionar_direita((a - self._subchaves[2 * rodada]) & self._mascara, b) ^ b
        return (a - self._subchaves[0]) & self._mascara, (b - self._subchaves[1]) & self._mascara

    def _processar(self, mensagem: str, operacao) -> str:
        bloco_bits = 2 * self._bits
        if not isinstance(mensagem, str):
            raise TypeError("A mensagem deve ser uma string binária.")
        if not mensagem or len(mensagem) % bloco_bits or any(bit not in "01" for bit in mensagem):
            raise ValueError(f"A mensagem deve conter blocos completos de {bloco_bits} bits (0 ou 1).")

        resultado = []
        for inicio in range(0, len(mensagem), bloco_bits):
            bloco = mensagem[inicio:inicio + bloco_bits]
            a = int(bloco[:self._bits], 2)
            b = int(bloco[self._bits:], 2)
            a, b = operacao(a, b)
            resultado.append(f"{a:0{self._bits}b}{b:0{self._bits}b}")
        return "".join(resultado)

    def cifrar_bits(self, mensagem: str) -> str:
        return self._processar(mensagem, self._cifrar_bloco)

    def decifrar_bits(self, cifra: str) -> str:
        return self._processar(cifra, self._decifrar_bloco)

    def cifrar(self, mensagem: str) -> str:
        return self.cifrar_bits(mensagem)

    def decifrar(self, cifra: str) -> str:
        return self.decifrar_bits(cifra)
