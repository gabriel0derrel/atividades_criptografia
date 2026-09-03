from criptolib import AritmeticaModular, TeoriaDosNumeros

class RSA:
    
    @staticmethod
    def gerar_chaves(p: int, q: int, e: int) -> tuple[tuple[int, int], tuple[int, int]]:
        # Retorna: ((e, n), (d, n))
        n = p * q
        phi_n = TeoriaDosNumeros.phi_de_euler(n)
        
        if TeoriaDosNumeros.euclides(e, phi_n) != 1:
            raise ValueError(f"O valor de 'e' ({e}) não é válido, pois MDC(e, phi(n)) != 1.")
            
        d = AritmeticaModular.inverso_modular(e, phi_n) # e^(-1) mod phi(n) = d
        
        chave_publica = (e, n)
        chave_privada = (d, n)
        
        return chave_publica, chave_privada

    @staticmethod
    def encriptar(mensagem: int, chave_publica: tuple[int, int]) -> int:
        # cifra = mensagem^e mod n
        e, n = chave_publica
        return AritmeticaModular.exponenciacao(mensagem, e, n)

    @staticmethod
    def decriptar(cifra: int, chave_privada: tuple[int, int]) -> int:
        # mensagem = cifra^d mod n
        d, n = chave_privada
        return AritmeticaModular.exponenciacao(cifra, d, n)


if __name__ == "__main__":
    # Seriam números de 2048 bits em um RSA real
    p = 61
    q = 53
    
    e = 17 # expoente público
    
    print("=== 1. Geração de Chaves ===")
    chave_pub, chave_priv = RSA.gerar_chaves(p, q, e)
    print(f"Primos escolhidos: p={p}, q={q}")
    print(f"Chave Pública (e, n) : {chave_pub}")
    print(f"Chave Privada (d, n) : {chave_priv}")
    
    mensagem_original = 65 # o valor numérico da mensagem deve ser estritamente menor que n
    print("\n=== 2. Mensagem Original ===")
    print(f"Mensagem (m): {mensagem_original}")
    
    cifra = RSA.encriptar(mensagem_original, chave_pub)
    print("\n=== 3. Encriptação ===")
    print(f"Texto Cifrado (c): {cifra}")
    
    mensagem_decriptada = RSA.decriptar(cifra, chave_priv)
    print("\n=== 4. Decriptação ===")
    print(f"Mensagem Restaurada (m'): {mensagem_decriptada}")
    
    assert mensagem_original == mensagem_decriptada, "Erro! A mensagem decriptada não bate com a original."