import sys
import time
import random

from abb import insert, search, delete, height
from datasets import (
    gerar_aleatorio,
    gerar_ordenado,
    gerar_quase_ordenado,
    montar_chaves_busca,
)

sys.setrecursionlimit(300_000)


class ABBWrapper:


    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = insert(self.root, key)

    def search(self, key):
        return search(self.root, key) is not None

    def delete(self, key):
        self.root = delete(self.root, key)

    def height(self):
        return height(self.root)


def executar_benchmark_estrutura(
    nome_estrutura,
    fabrica,
    chaves_base,
    m,
    k,
):

    n = len(chaves_base)
    estrutura = fabrica()

    inicio = time.perf_counter()
    for chave in chaves_base:
        estrutura.insert(chave)
    tempo_insercao_total = time.perf_counter() - inicio
    tempo_insercao_medio = tempo_insercao_total / n

    chaves_busca = montar_chaves_busca(chaves_base, m)
    inicio = time.perf_counter()
    for chave in chaves_busca:
        estrutura.search(chave)
    tempo_busca_total = time.perf_counter() - inicio
    tempo_busca_medio = tempo_busca_total / m

    chaves_remocao = random.sample(chaves_base, k)
    inicio = time.perf_counter()
    for chave in chaves_remocao:
        estrutura.delete(chave)
    tempo_remocao_total = time.perf_counter() - inicio
    tempo_remocao_medio = tempo_remocao_total / k

    altura_final = estrutura.height()

    return {
        "estrutura": nome_estrutura,
        "n": n,
        "tempo_medio_insercao": tempo_insercao_medio,
        "tempo_medio_busca": tempo_busca_medio,
        "tempo_medio_remocao": tempo_remocao_medio,
        "altura_final": altura_final,
    }


def main():
    random.seed(42)

    configuracoes = [
        ("aleatorio", gerar_aleatorio, 50_000),
        ("ordenado", gerar_ordenado, 30_000),
        ("quase_ordenado", gerar_quase_ordenado, 50_000),
    ]

    estruturas = {
        "ABB": lambda: ABBWrapper(),
    }

    resultados = []

    for nome_dataset, gerador, N in configuracoes:
        M = N        
        K = N // 10   

        chaves = gerador(N)

        print("\n====================================")
        print(f"DATASET: {nome_dataset}  (N={N}, M={M}, K={K})")
        print("====================================")

        for nome_estrutura, fabrica in estruturas.items():
            r = executar_benchmark_estrutura(
                nome_estrutura=nome_estrutura,
                fabrica=fabrica,
                chaves_base=chaves,
                m=M,
                k=K,
            )
            r["dataset"] = nome_dataset
            resultados.append(r)

            print(f"\nEstrutura: {r['estrutura']}")
            print(f"  Tempo médio inserção: {r['tempo_medio_insercao']:.6e} s")
            print(f"  Tempo médio busca   : {r['tempo_medio_busca']:.6e} s")
            print(f"  Tempo médio remoção : {r['tempo_medio_remocao']:.6e} s")
            print(f"  Altura final        : {r['altura_final']}")

    print("\n==================== RESUMO SIMPLES ====================")
    print("dataset        |     N | altura | t_ins | t_bus | t_rem (médios, em s)")
    for r in resultados:
        print(
            f"{r['dataset']:<13} | "
            f"{r['n']:>5} | "
            f"{r['altura_final']:>6} | "
            f"{r['tempo_medio_insercao']:.2e} | "
            f"{r['tempo_medio_busca']:.2e} | "
            f"{r['tempo_medio_remocao']:.2e}"
        )


if __name__ == "__main__":
    main()
