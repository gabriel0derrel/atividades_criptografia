class AritmeticaModular:

    @staticmethod
    def __validar_parametros(a: int, b: int, n: int | None = None) -> None:
        if type(a) is not int or type(b) is not int:
            raise TypeError("a e b devem ser inteiros.")

        if n is not None:
            if type(n) is not int:
                raise TypeError("n deve ser inteiro.")

            if n <= 0:
                raise ValueError("O módulo n deve ser um inteiro positivo (n > 0).")

    @staticmethod
    def adicao(a: int, b: int, n: int) -> int:
        AritmeticaModular.__validar_parametros(a, b, n)
        return (a + b) % n

    @staticmethod
    def subtracao(a: int, b: int, n: int) -> int:
        AritmeticaModular.__validar_parametros(a, b, n)
        return (a - b) % n

    @staticmethod
    def multiplicacao(a: int, b: int, n: int) -> int:
        AritmeticaModular.__validar_parametros(a, b, n)
        return (a * b) % n

    @staticmethod
    def divisao_modular(a: int, b: int, n: int) -> int:

        AritmeticaModular.__validar_parametros(a, b, n)

        if b == 0:
            raise ValueError(
                "Não é possível realizar divisão por zero."
            )

        inverso = AritmeticaModular.inverso_modular(b, n)

        return (a * inverso) % n

    @staticmethod
    def exponenciacao(a: int, b: int, n: int) -> int:
        AritmeticaModular.__validar_parametros(a, b, n)

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
    def mdc(a: int, b: int) -> int:
        AritmeticaModular.__validar_parametros(a, b)

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
        AritmeticaModular.__validar_parametros(a, b)

        a = abs(a)
        b = abs(b)

        if a == 0 and b == 0:
            raise ValueError("MDC(0, 0) não é definido.")

        while b != 0:
            a, b = b, a % b
        
        return a

    
    @staticmethod
    def euclides_estendido(a: int, b: int) -> tuple[int, int, int]:
        AritmeticaModular.__validar_parametros(a, b)

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
    def inverso_modular(a: int, n: int) -> int:

        return

