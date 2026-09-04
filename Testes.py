from criptolib import AritmeticaModular, TeoriaDosNumeros

def obter_inteiro(mensagem: str) -> int:
    """Função auxiliar para garantir que o usuário digite um número inteiro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("[ERRO DE DIGITAÇÃO] Por favor, digite um número inteiro válido.")

def menu_aritmetica_modular():
    while True:
        print("\n" + "="*30)
        print("=== SUB-MENU: ARITMÉTICA MODULAR ===")
        print("1. Adição (a + b mod n)")
        print("2. Subtração (a - b mod n)")
        print("3. Multiplicação (a * b mod n)")
        print("4. Divisão Modular (a / b mod n)")
        print("5. Potenciação (a^b mod n)")
        print("6. Inverso Modular (a^-1 mod n)")
        print("0. Voltar ao Menu Principal")
        print("="*30)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '0':
            break
            
        if opcao in ['1', '2', '3', '4', '5']:
            a = obter_inteiro("Digite o valor de a: ")
            b = obter_inteiro("Digite o valor de b: ")
            n = obter_inteiro("Digite o valor do módulo n: ")
            
            try:
                if opcao == '1':
                    print(f"\nResultado: {AritmeticaModular.adicao(a, b, n)}")
                elif opcao == '2':
                    print(f"\nResultado: {AritmeticaModular.subtracao(a, b, n)}")
                elif opcao == '3':
                    print(f"\nResultado: {AritmeticaModular.multiplicacao(a, b, n)}")
                elif opcao == '4':
                    print(f"\nResultado: {AritmeticaModular.divisao_modular(a, b, n)}")
                elif opcao == '5':
                    print(f"\nResultado: {AritmeticaModular.exponenciacao(a, b, n)}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")
                
        elif opcao == '6':
            a = obter_inteiro("Digite o valor de a: ")
            n = obter_inteiro("Digite o valor do módulo n: ")
            try:
                print(f"\nResultado: {AritmeticaModular.inverso_modular(a, n)}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")
        else:
            print("\nOpção inválida. Tente novamente.")


def menu_principal():
    while True:
        print("\n" + "="*30)
        print("=== MENU PRINCIPAL: CRIPTOLIB ===")
        print("1. Aritmética Modular (Sub-menu)")
        print("2. Verificar Número Primo")
        print("3. MDC por Tentativa")
        print("4. Algoritmo de Euclides")
        print("5. Euclides Estendido")
        print("6. Função Phi de Euler")
        print("7. Teorema Chinês do Resto")
        print("0. Sair")
        print("="*30)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '0':
            print("\nEncerrando o programa...")
            break
            
        elif opcao == '1':
            menu_aritmetica_modular()
            
        elif opcao == '2':
            num = obter_inteiro("Digite o número para verificar: ")
            try:
                resultado = TeoriaDosNumeros.e_primo(num)
                print(f"\nO número {num} é primo? {resultado}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")
                
        elif opcao in ['3', '4', '5']:
            a = obter_inteiro("Digite o valor de a: ")
            b = obter_inteiro("Digite o valor de b: ")
            try:
                if opcao == '3':
                    print(f"\nMDC({a}, {b}): {TeoriaDosNumeros.mdc(a, b)}")
                elif opcao == '4':
                    print(f"\nEuclides({a}, {b}): {TeoriaDosNumeros.euclides(a, b)}")
                elif opcao == '5':
                    mdc, x, y = TeoriaDosNumeros.euclides_estendido(a, b)
                    print(f"\nResultado -> MDC: {mdc} | x: {x} | y: {y}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")
                
        elif opcao == '6':
            n = obter_inteiro("Digite o valor de n para calcular ϕ(n): ")
            try:
                print(f"\nϕ({n}) = {TeoriaDosNumeros.phi_de_euler(n)}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")
                
        elif opcao == '7':
            try:
                qtd = obter_inteiro("Quantas congruências tem o sistema? ")
                if qtd <= 0:
                    print("\n[ERRO] O número de congruências deve ser positivo.")
                    continue
                    
                residuos = []
                modulos = []
                
                print("\nInsira os valores no formato (x ≡ resíduo mod módulo):")
                for i in range(qtd):
                    res = obter_inteiro(f"Resíduo {i+1}: ")
                    mod = obter_inteiro(f"Módulo {i+1}: ")
                    residuos.append(res)
                    modulos.append(mod)
                    
                resultado = AritmeticaModular.chines_resto(residuos, modulos)
                print(f"\nResultado: x = {resultado}")
            except Exception as erro:
                print(f"\n[ERRO NA OPERAÇÃO] {erro}")
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
