import math
from typing import Union, Tuple
from criptolib.utils.validacao import Validar


class InteiroModular:
    def __init__(self, valor: int, modulo: int):
        Validar.inteiros(valor)
        Validar.modulo(modulo)
        self.modulo = modulo
        self.valor = valor % modulo
        
    def __str__(self):
        return str(self.valor)

    def adicao(self, outro: Union["InteiroModular", int]) -> "InteiroModular":
        if isinstance(outro, InteiroModular):
            if self.modulo != outro.modulo:
                raise ValueError("Operações requerem elementos com o mesmo módulo.")
            b = outro.valor
        else:
            b = outro

        a, n = self.valor, self.modulo
        Validar.inteiros(a, b)
        Validar.modulo(n)
        return InteiroModular((a + b) % n, n)

    def subtracao(self, outro: Union["InteiroModular", int]) -> "InteiroModular":
        if isinstance(outro, InteiroModular):
            if self.modulo != outro.modulo:
                raise ValueError("Operações requerem elementos com o mesmo módulo.")
            b = outro.valor
        else:
            b = outro
        
        a, n = self.valor, self.modulo
        Validar.inteiros(a, b)
        Validar.modulo(n)
        return InteiroModular((a - b) % n, n)

    def multiplicacao(self, outro: Union["InteiroModular", int]) -> "InteiroModular":
        if isinstance(outro, InteiroModular):
            if self.modulo != outro.modulo:
                raise ValueError("Operações requerem elementos com o mesmo módulo.")
            b = outro.valor
        else:
            b = outro
        
        a, n = self.valor, self.modulo
        Validar.inteiros(a, b)
        Validar.modulo(n)
        return InteiroModular((a * b) % n, n)

    def divisao_modular(self, outro: Union["InteiroModular", int]) -> "InteiroModular":
        if isinstance(outro, InteiroModular):
            if self.modulo != outro.modulo:
                raise ValueError("Operações requerem elementos com o mesmo módulo.")
            b = outro.valor
        else:
            b = outro

        if b == 0:
            raise ValueError("Não é possível realizar divisão por zero.")
        
        a, n = self.valor, self.modulo
        Validar.inteiros(a, b)
        Validar.modulo(n)

        inverso = InteiroModular(b, n).inverso_modular().valor
        return InteiroModular((a * inverso) % n, n)

    def exponenciacao(self, b: int) -> "InteiroModular":
        a, n = self.valor, self.modulo
        Validar.inteiros(a, b)
        Validar.modulo(n)

        if b < 0:
            raise ValueError("O expoente b deve ser não negativo.")

        resultado = 1
        for i in range(b.bit_length() - 1, -1, -1):
            resultado = (resultado * resultado) % n
            if (b >> i) & 1 == 1:
                resultado = (resultado * a) % n

        return InteiroModular(resultado, n)

    def inverso_modular(self) -> "InteiroModular":
        a, n = self.valor, self.modulo
        Validar.inteiros(a)
        Validar.modulo(n)
        
        mdc, x, _ = InteiroModular.euclides_estendido(a, n)
        if mdc != 1:
            raise ValueError(f"O inverso modular de {a} mod {n} não existe pois MDC({a}, {n}) = {mdc} != 1.")

        return InteiroModular(x % n, n)

    @staticmethod
    def e_primo(numero: int) -> bool:
        Validar.inteiros(numero)
        if numero < 2: return False
        if numero == 2: return True
        if numero % 2 == 0: return False

        raiz_inteira = math.isqrt(numero)
        for divisor in range(3, raiz_inteira + 1, 2):
            if numero % divisor == 0: return False
        return True

    @staticmethod
    def mdc(a: int, b: int) -> int:
        Validar.inteiros(a, b)
        a, b = abs(a), abs(b)
        if a == 0 and b == 0:
            raise ValueError("MDC(0, 0) não é definido.")

        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def euclides_estendido(a: int, b: int) -> Tuple[int, int, int]:
        Validar.inteiros(a, b)
        if a == 0 and b == 0:
            raise ValueError("MDC(0, 0) não é definido.")

        sinal_a = 1 if a >= 0 else -1
        sinal_b = 1 if b >= 0 else -1

        resto_anterior, resto_atual = abs(a), abs(b)
        coeficiente_a_anterior, coeficiente_a_atual = 1, 0
        coeficiente_b_anterior, coeficiente_b_atual = 0, 1

        while resto_atual != 0:
            quociente = resto_anterior // resto_atual
            resto_anterior, resto_atual = resto_atual, (resto_anterior - quociente * resto_atual)
            coeficiente_a_anterior, coeficiente_a_atual = coeficiente_a_atual, (coeficiente_a_anterior - quociente * coeficiente_a_atual)
            coeficiente_b_anterior, coeficiente_b_atual = coeficiente_b_atual, (coeficiente_b_anterior - quociente * coeficiente_b_atual)

        return resto_anterior, coeficiente_a_anterior * sinal_a, coeficiente_b_anterior * sinal_b

    @staticmethod
    def phi_de_euler(n: int) -> int:
        Validar.modulo(n)
        resultado = n
        for i in range(2, math.isqrt(n) + 1):
            if n % i == 0:
                while n % i == 0:
                    n //= i
                resultado -= resultado // i

        if n > 1:
            resultado -= resultado // n
        return resultado
