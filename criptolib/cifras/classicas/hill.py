from criptolib.math import Matriz


class Hill:
    def __init__(self, chave: list[list[int]], alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        if not isinstance(alfabeto, str) or not alfabeto:
            raise ValueError("O alfabeto deve ser uma string não vazia.")
            
        self.alfabeto = alfabeto
        self.m = len(alfabeto)
        
        self.chave_matriz = Matriz(chave)
        self.n = len(self.chave_matriz.dados)
        
        self.chave_inversa = self.chave_matriz.inversa_modular(self.m)
        
        self._mapa_indices = {char: i for i, char in enumerate(alfabeto)}

    def _multiplicar_vetor_matriz(self, vetor: list[int], matriz: Matriz) -> list[int]:
        resultado = []
        for j in range(self.n):
            soma = sum(vetor[k] * matriz.dados[k][j] for k in range(self.n))
            resultado.append(soma % self.m)
        return resultado

    def cifrar(self, texto: str) -> str:
        texto_limpo = [c for c in texto.upper() if c in self._mapa_indices]
        
        padding = (self.n - len(texto_limpo) % self.n) % self.n
        texto_limpo.extend([self.alfabeto[0]] * padding)
        
        cifrado = []
        for i in range(0, len(texto_limpo), self.n):
            bloco_vetor = [self._mapa_indices[c] for c in texto_limpo[i:i + self.n]]
            bloco_cifrado = self._multiplicar_vetor_matriz(bloco_vetor, self.chave_matriz)
            cifrado.extend([self.alfabeto[idx] for idx in bloco_cifrado])
            
        return "".join(cifrado)

    def decifrar(self, cifra: str) -> str:
        cifra_limpa = [c for c in cifra.upper() if c in self._mapa_indices]
        
        if len(cifra_limpa) % self.n != 0:
            raise ValueError("O texto cifrado não possui um número de caracteres múltiplo do tamanho do bloco.")
            
        decifrado = []
        for i in range(0, len(cifra_limpa), self.n):
            bloco_vetor = [self._mapa_indices[c] for c in cifra_limpa[i:i + self.n]]
            bloco_decifrado = self._multiplicar_vetor_matriz(bloco_vetor, self.chave_inversa)
            decifrado.extend([self.alfabeto[idx] for idx in bloco_decifrado])
            
        return "".join(decifrado)
