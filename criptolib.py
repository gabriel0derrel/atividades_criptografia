def adicao_modular(a: int, b: int, n: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(n, int):
        raise TypeError("Os parâmetros a, b e n devem ser inteiros.")
    if n <= 0:
        raise ValueError("O módulo n deve ser um inteiro positivo (n > 0).")
    return (a + b) % n

def subtracao_modular(a: int, b: int, n: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(n, int):
        raise TypeError("Os parâmetros a, b e n devem ser inteiros.")
    if n <= 0:
        raise ValueError("O módulo n deve ser um inteiro positivo (n > 0).")
    return (a - b) % n

def multiplicacao_modular(a: int, b: int, n: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(n, int):
        raise TypeError("Os parâmetros a, b e n devem ser inteiros.")
    if n <= 0:
        raise ValueError("O módulo n deve ser um inteiro positivo (n > 0).")
    return (a * b) % n

def exponenciacao_modular(a: int, b: int, n: int) -> int:

    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(n, int):
        raise TypeError("Os parâmetros a, b e n devem ser inteiros.")

    if n <= 0:
        raise ValueError("O módulo n deve ser um inteiro positivo (n > 0).")

    if b < 0:
        raise ValueError("O expoente b deve ser não negativo.")

    d = 1

    # Representação binária do expoente
    bits = bin(b)[2:]

    for bit in bits:
        d = (d * d) % n

        if bit == "1":
            d = (d * a) % n

    return d


def mdc(a: int, b: int) -> int:

    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a e b devem ser inteiros.")

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