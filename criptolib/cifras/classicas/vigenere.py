class Vigenere:
    """Cifra de Vigenère sobre um alfabeto configurável.

    Caracteres que não pertencem ao alfabeto são preservados e não consomem
    posições da chave. A implementação é didática e não deve ser usada para
    proteger documentos reais.
    """

    def __init__(self, chave: str, alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        if not isinstance(chave, str) or not chave:
            raise ValueError("A chave deve ser uma string não vazia.")
        if not isinstance(alfabeto, str) or not alfabeto:
            raise ValueError("O alfabeto deve ser uma string não vazia.")
        if len(set(alfabeto)) != len(alfabeto):
            raise ValueError("O alfabeto não pode conter caracteres repetidos.")

        self.alfabeto = alfabeto
        self.n = len(alfabeto)
        self.chave = chave.upper()
        if not all(caractere in alfabeto for caractere in self.chave):
            raise ValueError("A chave deve conter apenas caracteres do alfabeto.")
        self._indices = {caractere: indice for indice, caractere in enumerate(alfabeto)}

    def _transformar(self, texto: str, sinal: int) -> str:
        if not isinstance(texto, str):
            raise TypeError("O texto deve ser uma string.")

        resultado = []
        indice_chave = 0
        for caractere in texto.upper():
            if caractere not in self._indices:
                resultado.append(caractere)
                continue
            valor = self._indices[caractere]
            deslocamento = self._indices[self.chave[indice_chave % len(self.chave)]]
            resultado.append(self.alfabeto[(valor + sinal * deslocamento) % self.n])
            indice_chave += 1
        return "".join(resultado)

    def cifrar(self, texto: str) -> str:
        return self._transformar(texto, 1)

    def decifrar(self, cifra: str) -> str:
        return self._transformar(cifra, -1)
