# Missão 3 — Cifras Modernas (SDES, DES, AES e RC5)

Esta pasta contém a prova de conceito referente à Missão 3. Ela engloba as implementações de **S-DES**, **DES**, **AES** e **RC5**, disponíveis no módulo `criptolib/cifras/modernas/`.

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

## Outras Cifras Suportadas

- **S-DES (Simplified DES):** Versão educacional simplificada com blocos de 8 bits e chave de 10 bits.
- **AES (Advanced Encryption Standard):** Cifra de bloco simétrica avançada com suporte a chaves de 128, 192 e 256 bits e blocos de 128 bits.
- **RC5:** Cifra de bloco parametrizável com tamanho de palavra variável, número configurável de rodadas e tamanho de chave flexível.

## Uso

```python
from criptolib.cifras.modernas import DES, SDES, AES, RC5

# Exemplo de uso com DES
chave = f"{int('133457799BBCDFF1', 16):064b}"
texto = f"{int('0123456789ABCDEF', 16):064b}"

cifra = DES(chave)
criptografado = cifra.cifrar_bits(texto)
original = cifra.decifrar_bits(criptografado)
```

Os métodos `cifrar_bits` e `decifrar_bits` recebem e devolvem strings binárias.
As mensagens devem ter tamanho múltiplo do tamanho de bloco do algoritmo correspondente. Os métodos `cifrar` e `decifrar` permanecem disponíveis como aliases para manter compatibilidade.

Para cifrar texto UTF-8, o método `cifrar_texto` retorna uma string hexadecimal contendo o vetor de inicialização (IV) seguido do texto cifrado em modo CBC. O método `decifrar_texto` recebe esse pacote e recupera o texto original. O preenchimento (padding) utilizado segue o padrão PKCS#7.

## Experimento com arquivos usando AES

Os métodos `cifrar_arquivo` e `decifrar_arquivo` permitem demonstrar o ciclo
arquivo original → AES → arquivo cifrado → AES → arquivo recuperado. O arquivo
cifrado contém o IV aleatório de 16 bytes seguido dos blocos cifrados. Os arquivos
originais não são modificados; use caminhos de saída diferentes.

```python
from criptolib.cifras.modernas import AES

chave = AES("0" * 128)
chave.cifrar_arquivo("documento.pdf", "documento.pdf.aes")
chave.decifrar_arquivo("documento.pdf.aes", "documento_recuperado.pdf")
```

Compare os bytes de `documento.pdf` e `documento_recuperado.pdf` para verificar
que o conteúdo foi recuperado sem alterações. O teste automatizado desse fluxo
pode ser executado com `py -m unittest discover -v`.

## Limitação de segurança

O DES e o S-DES são algoritmos legados/educacionais e não devem proteger documentos reais no SecureDocs. O DES possui chave efetiva de 56 bits vulnerável a busca exaustiva e blocos de 64 bits pequenos para grandes volumes. O modo CBC com IV aleatório sem autenticação associada não detecta alterações no pacote. Estas implementações servem apenas para estudo e validação dos algoritmos e não devem ser utilizadas em ambiente de produção.