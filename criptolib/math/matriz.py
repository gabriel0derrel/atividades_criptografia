from typing import Union
from criptolib.utils.validacao import Validar
from criptolib.math.modular import InteiroModular


class Matriz:
    def __init__(self, matriz: list[list[Union[int, float]]]):
        Validar.matriz_quadrada(matriz)
        self.dados = [linha[:] for linha in matriz]

    def determinante(self) -> int:
        matriz = [linha[:] for linha in self.dados]
        trocas = 0
        pivot_anterior = 1

        for i in range(len(matriz) - 1):
            pivot = matriz[i][i]
            if pivot == 0:
                for j in range(i + 1, len(matriz)):
                    if matriz[j][i] != 0:
                        matriz[i], matriz[j] = matriz[j], matriz[i]
                        trocas += 1
                        pivot = matriz[i][i]
                        break
                else:
                    return 0

            for j in range(i + 1, len(matriz)):
                for k in range(i + 1, len(matriz)):
                    matriz[j][k] = (matriz[j][k] * pivot - matriz[j][i] * matriz[i][k]) // pivot_anterior
            pivot_anterior = pivot
            for j in range(i + 1, len(matriz)):
                matriz[j][i] = 0

        determinante = matriz[-1][-1]
        if trocas % 2 != 0:
            determinante *= -1
        return determinante

    def modulo(self, n: int) -> "Matriz":
        Validar.modulo(n)
        Validar.inteiros(*(elemento for linha in self.dados for elemento in linha))
        
        matriz_mod = [[elemento % n for elemento in linha] for linha in self.dados]
        return Matriz(matriz_mod)

    def inversa(self) -> "Matriz":
        matriz = [linha[:] for linha in self.dados]
        tamanho = len(matriz)
        identidade = [[1 if i == j else 0 for j in range(tamanho)] for i in range(tamanho)]
        matriz_aumentada = [matriz[i] + identidade[i] for i in range(tamanho)]

        for i in range(tamanho):
            pivot = matriz_aumentada[i][i]
            if pivot == 0:
                for j in range(i + 1, tamanho):
                    if matriz_aumentada[j][i] != 0:
                        matriz_aumentada[i], matriz_aumentada[j] = matriz_aumentada[j], matriz_aumentada[i]
                        pivot = matriz_aumentada[i][i]
                        break
                else:
                    raise ValueError("A matriz não possui inversa.")

            for j in range(tamanho * 2):
                matriz_aumentada[i][j] = matriz_aumentada[i][j] / pivot

            for j in range(tamanho):
                if j == i: continue
                fator = matriz_aumentada[j][i]
                for k in range(tamanho * 2):
                    matriz_aumentada[j][k] = matriz_aumentada[j][k] - fator * matriz_aumentada[i][k]

        return Matriz([linha[tamanho:] for linha in matriz_aumentada])

    def inversa_modular(self, n: int) -> "Matriz":
        matriz = self.dados
        Validar.matriz_quadrada(matriz)
        Validar.modulo(n)
        Validar.inteiros(*(elemento for linha in matriz for elemento in linha))
        
        # Verificação de invertibilidade em módulo (Trazida pra cá)
        det = self.determinante()
        if InteiroModular.mdc(det, n) != 1:
            raise ValueError(f"A matriz não possui inversa modular em módulo {n}.")

        matriz_mod = [[elemento % n for elemento in linha] for linha in matriz]
        tamanho = len(matriz_mod)
        identidade = [[1 if i == j else 0 for j in range(tamanho)] for i in range(tamanho)]
        matriz_aumentada = [matriz_mod[i] + identidade[i] for i in range(tamanho)]

        for i in range(tamanho):
            pivot = matriz_aumentada[i][i]
            if InteiroModular.mdc(pivot, n) != 1:
                for j in range(i + 1, tamanho):
                    if InteiroModular.mdc(matriz_aumentada[j][i], n) == 1:
                        matriz_aumentada[i], matriz_aumentada[j] = matriz_aumentada[j], matriz_aumentada[i]
                        pivot = matriz_aumentada[i][i]
                        break

            inv_pivot = InteiroModular(pivot, n).inverso_modular().valor

            for j in range(tamanho * 2):
                matriz_aumentada[i][j] = (matriz_aumentada[i][j] * inv_pivot) % n

            for j in range(tamanho):
                if j == i: continue
                fator = matriz_aumentada[j][i]
                for k in range(tamanho * 2):
                    matriz_aumentada[j][k] = (matriz_aumentada[j][k] - fator * matriz_aumentada[i][k]) % n

        return Matriz([linha[tamanho:] for linha in matriz_aumentada])

    def multiplicacao(self, outra: Union["Matriz", list[list[Union[int, float]]]]) -> "Matriz":
        matriz_b = outra.dados if isinstance(outra, Matriz) else outra
        matriz_a = self.dados

        Validar.matriz_quadrada(matriz_b)

        if len(matriz_b) != len(matriz_a):
            raise ValueError("As matrizes devem ter dimensões compatíveis para a multiplicação.")

        n = len(matriz_a)
        resultado = []
        for i in range(n):
            linha = []
            for j in range(n):
                soma = sum(matriz_b[i][k] * matriz_a[k][j] for k in range(n))
                linha.append(soma)
            resultado.append(linha)

        return Matriz(resultado)

    def multiplicacao_modular(self, outra: Union["Matriz", list[list[Union[int, float]]]], n: int) -> "Matriz":
        return self.multiplicacao(outra).modulo(n)
