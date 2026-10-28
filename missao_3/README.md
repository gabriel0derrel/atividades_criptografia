# Missão 3 — DES

Esta pasta contém a prova de conceito da parte de DES da Missão 3. Ela implementa
somente o DES; AES e RC5 ficam fora deste escopo. A implementação está disponível
na biblioteca em `criptolib/cifras/modernas/des.py`.

## Como o DES funciona

O DES recebe blocos de 64 bits e uma chave representada por 64 bits. Oito bits da
chave são bits de paridade, então o tamanho efetivo da chave é 56 bits. A chave
passa por PC-1, é dividida em duas metades de 28 bits, sofre rotações à esquerda
e passa por PC-2 para gerar 16 subchaves de 48 bits.

Cada bloco passa pela permutação inicial e por 16 rodadas de Feistel. Em cada
rodada, a metade direita é expandida de 32 para 48 bits, combinada com a
subchave por XOR, processada pelas oito caixas S e permutada. Ao final, as
metades são trocadas e a permutação final é aplicada. A decifragem usa as mesmas
operações com as subchaves em ordem inversa.

## Uso

```python
from criptolib.cifras.modernas import Des

chave = f"{int('133457799BBCDFF1', 16):064b}"
texto = f"{int('0123456789ABCDEF', 16):064b}"

cifra = Des(chave)
criptografado = cifra.cifrar_bits(texto)
original = cifra.decifrar_bits(criptografado)
```

Os métodos `cifrar_bits` e `decifrar_bits` recebem e devolvem strings binárias.
As mensagens devem ter tamanho múltiplo de 64 bits. Os métodos `cifrar` e
`decifrar` permanecem disponíveis como aliases para manter compatibilidade.

Para cifrar texto UTF-8, `cifrar_texto` retorna uma string hexadecimal contendo
o IV de 8 bytes seguido do texto cifrado em CBC. `decifrar_texto` recebe esse
pacote e recupera o texto original. O padding utilizado é PKCS#7. O teste usa
o vetor conhecido que produz `85E813540F0AB405`.

## Limitação de segurança

DES é legado e não deve proteger documentos reais no SecureDocs: sua chave
efetiva de 56 bits é vulnerável a busca exaustiva e seu bloco de 64 bits é
pequeno para grandes volumes. CBC com IV aleatório não autentica o conteúdo nem
detecta alterações no pacote. Esta implementação serve apenas para estudo e
validação do algoritmo; não deve ser utilizada para proteger dados reais.

Execute os testes do repositório com:

```powershell
py -m unittest discover -v
```
