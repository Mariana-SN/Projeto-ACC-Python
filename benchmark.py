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

# para aumentar limite da recursão em caso ABB degenerada
sys.setrecursionlimit(300_000)


class ABBWrapper:


    def __init__(self):
        self.root = None

    def insert(self, key: int) -> None:
        self.root = insert(self.root, key)

    def search(self, key: int) -> bool:
        return search(self.root, key) is not None

    def delete(self, key: int) -> None:
        self.root = delete(self.root, key)

    def height(self) -> int:
        return height(self.root)

    def extra_metrics(self) -> dict:
        return {}


def executar_benchmark_estrutura(
    nome_estrutura: str,
    fabrica,
    chaves_base: list[int],
    m: int,
    k: int,
) -> dict:
 
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

    resultado = {
        "estrutura": nome_estrutura,
        "tempo_medio_insercao": tempo_insercao_medio,
        "tempo_medio_busca": tempo_busca_medio,
        "tempo_medio_remocao": tempo_remocao_medio,
        "altura_final": altura_final,
    }
    resultado.update(estrutura.extra_metrics())
    return resultado


def main():

    # usar um n entre 50.000 - 200.000 depois
    N = 50_000

    M = N                
    K = N // 10         

    random.seed(42)


    datasets = {
        "aleatorio": gerar_aleatorio(N),
        "ordenado": gerar_ordenado(N),
        "quase_ordenado": gerar_quase_ordenado(N),
    }

  
    estruturas = {
        "ABB": lambda: ABBWrapper(),
    }

    for nome_dataset, chaves in datasets.items():
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

            print(f"\nEstrutura: {r['estrutura']}")
            print(f"  Tempo médio inserção: {r['tempo_medio_insercao']:.6e} s")
            print(f"  Tempo médio busca   : {r['tempo_medio_busca']:.6e} s")
            print(f"  Tempo médio remoção : {r['tempo_medio_remocao']:.6e} s")
            print(f"  Altura final        : {r['altura_final']}")


if __name__ == "__main__":
    main()
