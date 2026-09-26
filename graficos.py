import matplotlib.pyplot as plt

RESULTADOS = [
    ("Facil\nft06 (6x6)",      90,     1.32,     291),
    ("Media\n8x6",            168,    60.41,   19975),
    ("Dificil\n10x10",        450,   600.90,  113733),
]


def comparativo(arquivo):
    nomes = [r[0] for r in RESULTADOS]
    cores = ["#2e7d32", "#f9a825", "#c62828"]
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.5))
    dados = [
        ([r[1] for r in RESULTADOS], "Variaveis binarias", False),
        ([r[2] for r in RESULTADOS], "Tempo (s) - escala log", True),
        ([r[3] for r in RESULTADOS], "Nos explorados (B&B) - escala log", True),
    ]
    for ax, (valores, titulo, log) in zip(axs, dados):
        barras = ax.bar(nomes, valores, color=cores, edgecolor="black")
        if log:
            ax.set_yscale("log")
        ax.set_title(titulo, fontweight="bold")
        for b, v in zip(barras, valores):
            ax.text(b.get_x() + b.get_width() / 2, v, f"{v:,}".replace(",", "."),
                    ha="center", va="bottom", fontsize=10)
        ax.margins(y=0.2)
    axs[1].text(2, RESULTADOS[2][2] * 0.35, "parou no\nlimite!", ha="center",
                color="white", fontweight="bold", fontsize=9)
    fig.suptitle("Binarias crescem 5x, tempo cresce mais de 450x (e sem provar o otimo)",
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(arquivo, dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    comparativo("comparativo.png")
    print("Grafico gerado: comparativo.png")
