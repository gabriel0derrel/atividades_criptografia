import math

class Validar:
    @staticmethod
    def inteiros(*valores: int) -> None:
        for valor in valores:
            if type(valor) is not int:
                raise TypeError("Todos os operandos devem ser inteiros.")

    @staticmethod
    def modulo(*modulos: int) -> None:
        Validar.inteiros(*modulos)
        for n in modulos:
            if n <= 0:
                raise ValueError("O módulo n deve ser um inteiro positivo (n > 0).")

    @staticmethod
    def coprimos_2_a_2(modulos: list[int]) -> None:
        for i in range(len(modulos)):
            for j in range(i + 1, len(modulos)):
                if math.gcd(modulos[i], modulos[j]) != 1:
                    raise ValueError(
                        f"Os módulos devem ser primos entre si 2 a 2. "
                        f"MDC({modulos[i]}, {modulos[j]}) != 1."
                    )

    @staticmethod
    def matriz_quadrada(matriz: list[list[int]]) -> None:
        if not isinstance(matriz, list) or not matriz:
            raise TypeError("A matriz deve ser uma lista não vazia.")

        if any(not isinstance(linha, list) for linha in matriz):
            raise TypeError("A matriz deve ser uma lista de listas.")

        if any(len(linha) != len(matriz[0]) for linha in matriz):
            raise ValueError("Todas as linhas da matriz devem possuir o mesmo tamanho.")

        if len(matriz) != len(matriz[0]):
            raise ValueError("A matriz deve ser quadrada.")
