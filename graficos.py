import csv
import matplotlib.pyplot as plt

ARQUIVO_CSV = "resultados_benchmark.csv"


def carregar_dados():
    dados = []
    with open(ARQUIVO_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            def to_float(value):
                return float(value) if value not in ("", None) else None

            row["tempo_medio_insercao"] = to_float(row["tempo_medio_insercao"])
            row["tempo_medio_busca"] = to_float(row["tempo_medio_busca"])
            row["tempo_medio_remocao"] = to_float(row["tempo_medio_remocao"])
            row["altura_final"] = to_float(row.get("altura_final"))
            row["rotacoes"] = to_float(row.get("rotacoes"))
            row["colisoes_totais"] = to_float(row.get("colisoes_totais"))
            dados.append(row)
    return dados


def grafico_barras_simples(dados, campo, dataset, nome_arquivo, titulo_y):

    filtrados = [d for d in dados if d["dataset"] == dataset and d[campo] is not None]

    estruturas = [d["estrutura"] for d in filtrados]
    valores = [d[campo] for d in filtrados]

    plt.figure()
    plt.bar(estruturas, valores)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(titulo_y)
    plt.title(f"{titulo_y} – dataset {dataset}")
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()


def grafico_altura_arvores(dados, nome_arquivo):
    """
    Compara a altura final de ABB e AVL por dataset.
    Usa escala logarítmica no eixo Y para que a ABB (muito alta em dados ordenados)
    e a AVL (altura pequena) apareçam juntas de forma legível.
    """
    datasets = sorted(set(d["dataset"] for d in dados))
    estruturas = ["ABB", "AVL"]

    plt.figure()
    for estrutura in estruturas:
        xs = []
        ys = []
        for ds in datasets:
            reg = next(
                (
                    d
                    for d in dados
                    if d["dataset"] == ds
                    and d["estrutura"] == estrutura
                    and d["altura_final"] is not None
                ),
                None,
            )
            if reg:
                xs.append(ds)
                ys.append(reg["altura_final"])

        if xs and ys:
            plt.plot(xs, ys, marker="o", label=estrutura)

    plt.ylabel("Altura da árvore (escala log)")
    plt.yscale("log") 
    plt.title("Altura final de ABB e AVL por dataset")
    plt.legend()
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()


def grafico_colisoes_hash(dados, dataset, nome_arquivo):

    filtrados = [
        d
        for d in dados
        if d["dataset"] == dataset and d["colisoes_totais"] is not None
    ]

    estruturas = [d["estrutura"] for d in filtrados]
    valores = [d["colisoes_totais"] for d in filtrados]

    plt.figure()
    plt.bar(estruturas, valores)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Colisões totais")
    plt.title(f"Colisões em tabelas hash – dataset {dataset}")
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()


def grafico_rotacoes_avl(dados, nome_arquivo):

    filtrados = [
        d for d in dados if d["estrutura"] == "AVL" and d["rotacoes"] is not None
    ]

    datasets = [d["dataset"] for d in filtrados]
    valores = [d["rotacoes"] for d in filtrados]

    plt.figure()
    plt.bar(datasets, valores)
    plt.ylabel("Quantidade de rotações")
    plt.title("Rotações na árvore AVL por dataset")
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()


if __name__ == "__main__":
    dados = carregar_dados()

    for ds in ("aleatorio", "ordenado", "quase_ordenado"):
        grafico_barras_simples(
            dados,
            campo="tempo_medio_insercao",
            dataset=ds,
            nome_arquivo=f"tempo_insercao_{ds}.png",
            titulo_y="Tempo médio de inserção (s)",
        )
        grafico_barras_simples(
            dados,
            campo="tempo_medio_busca",
            dataset=ds,
            nome_arquivo=f"tempo_busca_{ds}.png",
            titulo_y="Tempo médio de busca (s)",
        )
        grafico_barras_simples(
            dados,
            campo="tempo_medio_remocao",
            dataset=ds,
            nome_arquivo=f"tempo_remocao_{ds}.png",
            titulo_y="Tempo médio de remoção (s)",
        )

    grafico_altura_arvores(dados, "altura_arvores.png")

    grafico_colisoes_hash(
        dados,
        dataset="aleatorio",
        nome_arquivo="colisoes_hash_aleatorio.png",
    )

    grafico_rotacoes_avl(dados, "rotacoes_avl.png")

    print("Arquivos dos gráficos gerados na pasta do projeto.")
