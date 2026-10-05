class Substituicao:
    """Cifra monoalfabética de substituição simples."""

    def __init__(
        self,
        chave: str,
        alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    ):
        if not isinstance(chave, str):
            raise TypeError("A chave deve ser uma string.")
        if not isinstance(alfabeto, str) or not alfabeto:
            raise ValueError("O alfabeto deve ser uma string não vazia.")
        if len(set(alfabeto)) != len(alfabeto):
            raise ValueError("O alfabeto não pode conter caracteres repetidos.")

        chave = chave.upper()
        if len(chave) != len(alfabeto):
            raise ValueError("A chave deve ter o mesmo tamanho do alfabeto.")
        if set(chave) != set(alfabeto):
            raise ValueError("A chave deve ser uma permutação do alfabeto.")

        self.alfabeto = alfabeto
        self.chave = chave
        self._cifrar = dict(zip(alfabeto, chave))
        self._decifrar = dict(zip(chave, alfabeto))

    def _transformar(self, texto: str, mapa: dict[str, str]) -> str:
        if not isinstance(texto, str):
            raise TypeError("O texto deve ser uma string.")
        return "".join(mapa.get(caractere.upper(), caractere) for caractere in texto)

    def cifrar(self, texto: str) -> str:
        return self._transformar(texto, self._cifrar)

    def decifrar(self, cifra: str) -> str:
        return self._transformar(cifra, self._decifrar)
