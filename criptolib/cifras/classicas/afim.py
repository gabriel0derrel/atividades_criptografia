from criptolib.utils.validacao import Validar
from criptolib.math import InteiroModular

class Afim:
    def __init__(self, chave_a: int, chave_b: int, alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        Validar.inteiros(chave_a, chave_b)
        
        if not isinstance(alfabeto, str) or not alfabeto:
            raise ValueError("O alfabeto deve ser uma string não vazia.")

        self.alfabeto = alfabeto
        self.n = len(alfabeto)
        
        if InteiroModular.mdc(chave_a, self.n) != 1:
            raise ValueError(f"A chave 'a' ({chave_a}) e o tamanho do alfabeto ({self.n}) não são coprimos. Escolha outro valor para 'a'.")

        self.a = chave_a
        self.b = chave_b
        
        self.a_inv = InteiroModular(self.a, self.n).inverso_modular().valor 
        
        self._mapa_indices = {char: i for i, char in enumerate(alfabeto)}

    def cifrar(self, texto: str) -> str:
        resultado = []
        for char in texto.upper():
            if char in self._mapa_indices:
                x = self._mapa_indices[char]
                y = (self.a * x + self.b) % self.n
                resultado.append(self.alfabeto[y])
            else:
                resultado.append(char)
        return "".join(resultado)

    def decifrar(self, cifra: str) -> str:
        resultado = []
        for char in cifra.upper():
            if char in self._mapa_indices:
                y = self._mapa_indices[char]
                x = (self.a_inv * (y - self.b)) % self.n
                resultado.append(self.alfabeto[x])
            else:
                resultado.append(char)
        return "".join(resultado)
