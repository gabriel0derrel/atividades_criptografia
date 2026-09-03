from criptolib import AritmeticaModular, TeoriaDosNumeros


print("=== ARITMÉTICA MODULAR ===")

a = 17
b = 8
n = 5

print(f"Adição: {a} + {b} mod {n} =", AritmeticaModular.adicao(a, b, n))

print(f"Subtração: {a} - {b} mod {n} =", AritmeticaModular.subtracao(a, b, n))

print(f"Multiplicação: {a} * {b} mod {n} =", AritmeticaModular.multiplicacao(a, b, n))

print(f"Divisão Modular: {a} / {b} mod {n} =", AritmeticaModular.divisao_modular(a, b, n))

print(f"Potenciação: {a}^{b} mod {n} =", AritmeticaModular.exponenciacao(a, b, n))
print(f"Potenciação Bruta: ({a}**{b}) % {n} =", (a**b)%n)

print(f"Inverso Modular: {a}^(-1) mod {n} =", AritmeticaModular.inverso_modular(a, n))

print("\n=== MDC POR TENTATIVA ===")

print("MDC(60, 24):", TeoriaDosNumeros.mdc(60, 24))

print("MDC(-60, 24):", TeoriaDosNumeros.mdc(-60, 24))

print("MDC(25, 0):", TeoriaDosNumeros.mdc(25, 0))


print("\n=== ALGORITMO DE EUCLIDES ===")

print("Euclides(60, 24):", TeoriaDosNumeros.euclides(60, 24))

print("Euclides(-60, 24):", TeoriaDosNumeros.euclides(-60, 24))

print("Euclides(25, 0):", TeoriaDosNumeros.euclides(25, 0))


print("\n=== EUCLIDES ESTENDIDO ===")

mdc, x, y = TeoriaDosNumeros.euclides_estendido(60, 24)

print("Entrada: a = 60, b = 24")
print("MDC:", mdc)
print("x:", x)
print("y:", y)
print(f"Verificação: 60 * ({x}) + 24 * ({y}) =", 60 * x + 24 * y)

mdc, x, y = TeoriaDosNumeros.euclides_estendido(-60, 24)

print("\nEntrada: a = -60, b = 24")
print("MDC:", mdc)
print("x:", x)
print("y:", y)
print(f"Verificação: (-60) * ({x}) + 24 * ({y}) =", -60 * x + 24 * y)

print("\n=== FUNÇÃO PHI DE EULER ===")

print("ϕ(4) =", TeoriaDosNumeros.phi_de_euler(4))
print("ϕ(7) =", TeoriaDosNumeros.phi_de_euler(7))
print("ϕ(10) =", TeoriaDosNumeros.phi_de_euler(10))
print("ϕ(26) =", TeoriaDosNumeros.phi_de_euler(26))
print("ϕ(32) =", TeoriaDosNumeros.phi_de_euler(32))

print("\n=== TEOREMA CHINÊS DO RESTO ===")

residuos = [4, 3, 5]
modulos = [5, 7, 16]

print(f"x ≡ {residuos[0]} mod {modulos[0]}")
print(f"x ≡ {residuos[1]} mod {modulos[1]}")
print(f"x ≡ {residuos[2]} mod {modulos[2]}")
print(f"Resultado: x =", AritmeticaModular.chines_resto(residuos, modulos))
