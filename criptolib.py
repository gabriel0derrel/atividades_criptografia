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

class AritmeticaModular:

    @staticmethod
    def adicao(a: int, b: int, n: int) -> int:
        Validar.inteiros(a, b)
        Validar.modulo(n)
        return (a + b) % n

    @staticmethod
    def subtracao(a: int, b: int, n: int) -> int:
        Validar.inteiros(a, b)
        Validar.modulo(n)
        return (a - b) % n

    @staticmethod
    def multiplicacao(a: int, b: int, n: int) -> int:
        Validar.inteiros(a, b)
        Validar.modulo(n)
        return (a * b) % n

    @staticmethod
    def divisao_modular(a: int, b: int, n: int) -> int:
        Validar.inteiros(a, b)
        Validar.modulo(n)

        if b == 0:
            raise ValueError(
                "Não é possível realizar divisão por zero."
            )

        inverso = AritmeticaModular.inverso_modular(b, n)

        return (a * inverso) % n

    @staticmethod
    def exponenciacao(a: int, b: int, n: int) -> int:
        Validar.inteiros(a, b)
        Validar.modulo(n)

        if b < 0:
            raise ValueError("O expoente b deve ser não negativo.")

        resultado = 1
        bits = bin(b)[2:]

        for bit in bits:
            resultado = (resultado * resultado) % n

            if bit == "1":
                resultado = (resultado * a) % n

        return resultado

    @staticmethod
    def inverso_modular(a: int, n: int) -> int:
        Validar.inteiros(a)
        Validar.modulo(n)
        mdc, x, _ = TeoriaDosNumeros.euclides_estendido(a, n)
        
        if mdc != 1:
            raise ValueError(f"O inverso modular de {a} mod {n} não existe pois MDC({a}, {n}) = {mdc} != 1.")
            
        return x % n

    @staticmethod
    def chines_resto(residuos: list[int], modulos: list[int]) -> int:
        Validar.inteiros(*residuos)
        Validar.modulo(*modulos)

        m = math.prod(modulos)
        m_i = [m // modulo for modulo in modulos]
        m_i_inv = [AritmeticaModular.inverso_modular(m_i_aux, modulo) for m_i_aux, modulo in zip(m_i, modulos)]

        resposta = sum(residuo*m_i_aux*m_i_inv_aux for residuo, m_i_aux, m_i_inv_aux in zip(residuos, m_i, m_i_inv))
        resposta %= m
        return resposta


class TeoriaDosNumeros:

    @staticmethod
    def e_primo(numero: int) -> bool:
        # Pendente
        return

    @staticmethod
    def mdc(a: int, b: int) -> int:
        Validar.inteiros(a, b)

        a = abs(a)
        b = abs(b)

        if a == 0 and b == 0:
            raise ValueError("MDC(0, 0) não é definido.")

        if a == 0:
            return b

        if b == 0:
            return a

        limite = min(a, b)

        for k in range(limite, 0, -1):
            if a % k == 0 and b % k == 0:
                return k

        return 1


    @staticmethod
    def euclides(a: int, b: int) -> int:
        Validar.inteiros(a, b)

        a = abs(a)
        b = abs(b)

        if a == 0 and b == 0:
            raise ValueError("MDC(0, 0) não é definido.")

        while b != 0:
            a, b = b, a % b
        
        return a

    
    @staticmethod
    def euclides_estendido(a: int, b: int) -> tuple[int, int, int]:
        Validar.inteiros(a, b)

        if a == 0 and b == 0:
            raise ValueError("MDC(0, 0) não é definido.")

        sinal_a = 1 if a >= 0 else -1
        sinal_b = 1 if b >= 0 else -1

        resto_anterior = abs(a)
        resto_atual = abs(b)

        coeficiente_a_anterior = 1
        coeficiente_a_atual = 0

        coeficiente_b_anterior = 0
        coeficiente_b_atual = 1

        while resto_atual != 0:
            quociente = resto_anterior // resto_atual

            resto_anterior, resto_atual = (
                resto_atual,
                resto_anterior - quociente * resto_atual
            )

            coeficiente_a_anterior, coeficiente_a_atual = (
                coeficiente_a_atual,
                coeficiente_a_anterior - quociente * coeficiente_a_atual
            )

            coeficiente_b_anterior, coeficiente_b_atual = (
                coeficiente_b_atual,
                coeficiente_b_anterior - quociente * coeficiente_b_atual
            )

        mdc = resto_anterior

        x = coeficiente_a_anterior * sinal_a
        y = coeficiente_b_anterior * sinal_b

        return mdc, x, y

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
