class Transposicao:
    def __init__(self, chave: str, alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        if not isinstance(chave, str) or not chave:
            raise ValueError("A chave deve ser uma string não vazia.")

        if not isinstance(alfabeto, str) or not alfabeto:
            raise ValueError("O alfabeto deve ser uma string não vazia.")

        self.chave = chave.upper().replace(" ", "")
        self.alfabeto = alfabeto

        if not all(char in self.alfabeto for char in self.chave):
            raise ValueError("A chave deve conter apenas caracteres do alfabeto.")

        if len(set(self.chave)) != len(self.chave):
            raise ValueError("A chave não pode possuir caracteres repetidos.")

    def _obter_ordem_colunas(self) -> list[int]:
        return sorted(
            range(len(self.chave)),
            key=lambda i: self.chave[i]
        )

    def cifrar(self, texto: str) -> str:
        texto_limpo = [
            char for char in texto.upper()
            if char in self.alfabeto
        ]

        numero_colunas = len(self.chave)

        padding = (
            numero_colunas - len(texto_limpo) % numero_colunas
        ) % numero_colunas

        texto_limpo.extend(["X"] * padding)

        linhas = []

        for i in range(0, len(texto_limpo), numero_colunas):
            linhas.append(texto_limpo[i:i + numero_colunas])

        ordem_colunas = self._obter_ordem_colunas()

        cifrado = []

        for coluna in ordem_colunas:
            for linha in linhas:
                cifrado.append(linha[coluna])

        return "".join(cifrado)

    def decifrar(self, cifra: str) -> str:
        cifra_limpa = [
            char for char in cifra.upper()
            if char in self.alfabeto
        ]

        numero_colunas = len(self.chave)

        if len(cifra_limpa) % numero_colunas != 0:
            raise ValueError(
                "O texto cifrado não possui um número de caracteres "
                "múltiplo do tamanho da chave."
            )

        numero_linhas = len(cifra_limpa) // numero_colunas
        ordem_colunas = self._obter_ordem_colunas()

        matriz = [
            [""] * numero_colunas
            for _ in range(numero_linhas)
        ]

        posicao = 0

        for coluna in ordem_colunas:
            for linha in range(numero_linhas):
                matriz[linha][coluna] = cifra_limpa[posicao]
                posicao += 1

        decifrado = []

        for linha in matriz:
            decifrado.extend(linha)

        return "".join(decifrado).rstrip("X")