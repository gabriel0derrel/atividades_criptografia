from criptolib import (
    adicao_modular,
    subtracao_modular,
    multiplicacao_modular,
    exponenciacao_modular,
    mdc
)

print("=== ARITMÉTICA MODULAR ===")

print("Adição: 17 + 8 mod 5 = ", adicao_modular(17, 8, 5))
print("Subtração: 17 - 8 mod 5 = ", subtracao_modular(17, 8, 5))
print("Multiplicação: 17 * 8 mod 5 = ", multiplicacao_modular(17, 8, 5))
print("Potenciação: 17^8 mod 5 = ", exponenciacao_modular(11, 7, 13))

print("\n=== MDC ===")

print("MDC(60, 24):", mdc(60, 24))
print("MDC(-60, 24):", mdc(-60, 24))
print("MDC(25, 0):", mdc(25, 0))