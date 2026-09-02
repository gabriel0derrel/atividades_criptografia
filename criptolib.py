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

        a_abs = abs(a)
        b_abs = abs(b)

        if a_abs == 0 and b_abs == 0:
            raise ValueError("MDC(0, 0) não é definido.")

        if a_abs == 0:
            return b_abs

        if b_abs == 0:
            return a_abs

        limite = min(a_abs, b_abs)

        for k in range(limite, 0, -1):
            if a_abs % k == 0 and b_abs % k == 0:
                return k

        return 1

