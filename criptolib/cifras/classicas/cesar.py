from criptolib.utils.validacao import Validar


class Cesar:
    def __init__(self, chave: int, alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        Validar.inteiros(chave)
        if not isinstance(alfabeto, str) or not alfabeto:
            raise ValueError("O alfabeto deve ser uma string não vazia.")

        self.alfabeto = alfabeto
        self.n = len(alfabeto)
        self.chave = chave
        self._mapa_indices = {char: i for i, char in enumerate(alfabeto)}

    def cifrar(self, texto: str) -> str:
        resultado = []
        for char in texto.upper():
            if char in self._mapa_indices:
                x = self._mapa_indices[char]
                y = (x + self.chave) % self.n
                resultado.append(self.alfabeto[y])
            else:
                resultado.append(char)
        return "".join(resultado)

    def decifrar(self, cifra: str) -> str:
        resultado = []
        for char in cifra.upper():
            if char in self._mapa_indices:
                y = self._mapa_indices[char]
                x = (y - self.chave) % self.n
                resultado.append(self.alfabeto[x])
            else:
                resultado.append(char)
        return "".join(resultado)
