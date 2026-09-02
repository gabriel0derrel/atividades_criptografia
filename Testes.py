from criptolib import (
    AritmeticaModular
)

print("=== ARITMÉTICA MODULAR ===")

print("Adição: 17 + 8 mod 5 =", AritmeticaModular.adicao(17, 8, 5))
print("Subtração: 17 - 8 mod 5 =", AritmeticaModular.subtracao(17, 8, 5))
print("Multiplicação: 17 * 8 mod 5 =" , AritmeticaModular.multiplicacao(17, 8, 5))
print("Potenciação: 17^8 mod 5 =", AritmeticaModular.exponenciacao(11, 7, 13))

print("\n=== MDC ===")

print("MDC(60, 24):", AritmeticaModular.mdc(60, 24))
print("MDC(-60, 24):", AritmeticaModular.mdc(-60, 24))
print("MDC(25, 0):", AritmeticaModular.mdc(25, 0))