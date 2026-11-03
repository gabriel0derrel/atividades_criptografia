from pathlib import Path
import string
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from criptolib.cifras.modernas import AES


_PASTA_PROJETO = Path(__file__).resolve().parent
_PASTA_CIFRADOS = _PASTA_PROJETO / "arquivos_cifrados"
_PASTA_RECUPERADOS = _PASTA_PROJETO / "arquivos_recuperados"


def _solicitar_cifra(janela: tk.Tk) -> AES | None:
    chave_hex = simpledialog.askstring(
        "Chave AES",
        "Digite a chave hexadecimal de 32, 48 ou 64 caracteres:",
        show="*",
        parent=janela,
    )
    if chave_hex is None:
        return None

    chave_hex = chave_hex.strip()
    if (
        len(chave_hex) not in (32, 48, 64)
        or any(caractere not in string.hexdigits for caractere in chave_hex)
    ):
        messagebox.showerror(
            "Chave inválida",
            "A chave deve ter 32, 48 ou 64 caracteres hexadecimais.",
            parent=janela,
        )
        return None

    chave_bits = f"{int(chave_hex, 16):0{len(chave_hex) * 4}b}"
    return AES(chave_bits)


def _caminho_disponivel(pasta: Path, nome: str) -> Path:
    destino = pasta / nome
    indice = 1
    while destino.exists():
        destino = pasta / f"{Path(nome).stem} ({indice}){Path(nome).suffix}"
        indice += 1
    return destino


def _cifrar_arquivo(janela: tk.Tk) -> None:
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo para cifrar",
        filetypes=(("Todos os arquivos", "*.*"),),
        parent=janela,
    )
    if not arquivo:
        return

    cifra = _solicitar_cifra(janela)
    if cifra is None:
        return

    entrada = Path(arquivo)
    try:
        _PASTA_CIFRADOS.mkdir(parents=True, exist_ok=True)
        saida = _caminho_disponivel(
            _PASTA_CIFRADOS,
            f"{entrada.name}.sdocaes",
        )
        cifra.cifrar_arquivo(entrada, saida)
    except OSError as erro:
        messagebox.showerror("Erro ao cifrar", str(erro), parent=janela)
        return

    messagebox.showinfo(
        "Arquivo cifrado",
        f"Arquivo salvo em:\n{saida}",
        parent=janela,
    )


def _decifrar_arquivo(janela: tk.Tk) -> None:
    arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo cifrado SecureDocs",
        filetypes=(
            ("Arquivos cifrados SecureDocs", "*.sdocaes"),
            ("Todos os arquivos", "*.*"),
        ),
        parent=janela,
    )
    if not arquivo:
        return

    cifra = _solicitar_cifra(janela)
    if cifra is None:
        return

    entrada = Path(arquivo)
    nome_original = entrada.name.removesuffix(".sdocaes")
    try:
        _PASTA_RECUPERADOS.mkdir(parents=True, exist_ok=True)
        saida = _caminho_disponivel(_PASTA_RECUPERADOS, nome_original)
        cifra.decifrar_arquivo(entrada, saida)
    except (OSError, ValueError) as erro:
        messagebox.showerror("Não foi possível decifrar", str(erro), parent=janela)
        return

    messagebox.showinfo(
        "Arquivo recuperado",
        f"Arquivo salvo em:\n{saida}",
        parent=janela,
    )


def main() -> None:
    janela = tk.Tk()
    janela.title("Demonstração de arquivos com AES")
    janela.resizable(False, False)

    conteudo = ttk.Frame(janela, padding=20)
    conteudo.grid()

    ttk.Label(
        conteudo,
        text=(
            "Selecione um arquivo para cifrar ou um arquivo .sdocaes para "
            "decifrar.\nOs arquivos de saída são salvos em pastas separadas "
            "na pasta do projeto."
        ),
        justify="center",
        wraplength=420,
    ).grid(row=0, column=0, columnspan=2, pady=(0, 16))

    ttk.Button(
        conteudo,
        text="Selecionar arquivo para cifrar",
        command=lambda: _cifrar_arquivo(janela),
    ).grid(row=1, column=0, padx=5)

    ttk.Button(
        conteudo,
        text="Selecionar arquivo para decifrar",
        command=lambda: _decifrar_arquivo(janela),
    ).grid(row=1, column=1, padx=5)

    janela.mainloop()


if __name__ == "__main__":
    main()
