from criptolib.utils.validacao import Validar

class AutoChave:
    def __init__( self, chave: str | int, alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        if not isinstance(alfabeto, str) or not alfabeto:
            raise ValueError("O alfabeto deve ser uma string não vazia.")

        if len(set(alfabeto)) != len(alfabeto):
            raise ValueError("O alfabeto não pode conter caracteres repetidos.")

        if isinstance(chave, int):
            Validar.inteiros(chave)

            if chave < 0 or chave >= len(alfabeto):
                raise ValueError("O inteiro da chave deve corresponder a uma posição válida do alfabeto.")

            chave = alfabeto[chave]

        elif isinstance(chave, str):
            if len(chave) != 1:
                raise ValueError("A chave deve possuir exatamente um caractere.")

            chave = chave.upper()

            if chave not in alfabeto:
                raise ValueError("O caractere da chave deve pertencer ao alfabeto.")

        else:
            raise TypeError("A chave deve ser um caractere ou um inteiro.")

        self.alfabeto = alfabeto
        self.n = len(alfabeto)
        self.chave = chave

        self._mapa_indices = {char: i for i, char in enumerate(alfabeto)}

    def cifrar(self, texto: str) -> str:
        if not isinstance(texto, str):
            raise TypeError("O texto deve ser uma string.")

        texto_limpo = [char for char in texto.upper() if char in self._mapa_indices]

        resultado = []

        for i, char in enumerate(texto_limpo):
            indice_texto = self._mapa_indices[char]

            if i == 0:
                indice_chave = self._mapa_indices[self.chave]
            else:
                indice_chave = self._mapa_indices[texto_limpo[i - 1]]

            indice_cifrado = (indice_texto + indice_chave) % self.n

            resultado.append(self.alfabeto[indice_cifrado])

        return "".join(resultado)

    def decifrar(self, cifra: str) -> str:
        if not isinstance(cifra, str):
            raise TypeError("A cifra deve ser uma string.")

        cifra_limpa = [char for char in cifra.upper() if char in self._mapa_indices]

        resultado = []
        texto_decifrado = []

        for i, char in enumerate(cifra_limpa):
            indice_cifra = self._mapa_indices[char]

            if i == 0:
                indice_chave = self._mapa_indices[self.chave]
            else:
                indice_chave = self._mapa_indices[texto_decifrado[i - 1]]

            indice_original = (indice_cifra - indice_chave) % self.n

            char_original = self.alfabeto[indice_original]

            resultado.append(char_original)
            texto_decifrado.append(char_original)

        return "".join(resultado)
