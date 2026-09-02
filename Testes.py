from criptolib import AritmeticaModular


print("=== ARITMÉTICA MODULAR ===")

a = 17
b = 8
n = 5

print(f"Adição: {a} + {b} mod {n} =", 
      AritmeticaModular.adicao(a, b, n))

print(f"Subtração: {a} - {b} mod {n} =", 
      AritmeticaModular.subtracao(a, b, n))

print(f"Multiplicação: {a} * {b} mod {n} =", 
      AritmeticaModular.multiplicacao(a, b, n))

print(f"Potenciação: {a}^{b} mod {n} =", 
      AritmeticaModular.exponenciacao(a, b, n))


print("\n=== MDC POR TENTATIVA ===")

print("MDC(60, 24):", 
      AritmeticaModular.mdc(60, 24))

print("MDC(-60, 24):", 
      AritmeticaModular.mdc(-60, 24))

print("MDC(25, 0):", 
      AritmeticaModular.mdc(25, 0))


print("\n=== ALGORITMO DE EUCLIDES ===")

print("Euclides(60, 24):", 
      AritmeticaModular.euclides(60, 24))

print("Euclides(-60, 24):", 
      AritmeticaModular.euclides(-60, 24))

print("Euclides(25, 0):", 
      AritmeticaModular.euclides(25, 0))


print("\n=== EUCLIDES ESTENDIDO ===")

mdc, x, y = AritmeticaModular.euclides_estendido(60, 24)

print("Entrada: a = 60, b = 24")
print("MDC:", mdc)
print("x:", x)
print("y:", y)
print(f"Verificação: 60 * ({x}) + 24 * ({y}) =", 60 * x + 24 * y)

mdc, x, y = AritmeticaModular.euclides_estendido(-60, 24)

print("\nEntrada: a = -60, b = 24")
print("MDC:", mdc)
print("x:", x)
print("y:", y)
print(f"Verificação: (-60) * ({x}) + 24 * ({y}) =", -60 * x + 24 * y)