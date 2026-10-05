import random

from criptolib.utils.validacao import Validar


class Fluxo:
    def __init__(self, seed: int):
        Validar.inteiros(seed)
        self.seed = seed

    def cifrar(self, texto: str) -> str:
        if not isinstance(texto, str):
            raise TypeError("O texto deve ser uma string.")

        gerador = random.Random(self.seed)
        dados = texto.encode("utf-8")
        cifrado = bytes(
            byte ^ gerador.getrandbits(8)
            for byte in dados
        )
        return cifrado.hex()

    def decifrar(self, cifra: str) -> str:
        if not isinstance(cifra, str):
            raise TypeError("A cifra deve ser uma string hexadecimal.")

        try:
            dados = bytes.fromhex(cifra)
        except ValueError as erro:
            raise ValueError("A cifra deve conter uma string hexadecimal válida.") from erro

        gerador = random.Random(self.seed)
        decifrado = bytes(
            byte ^ gerador.getrandbits(8)
            for byte in dados
        )
        return decifrado.decode("utf-8")