import sys
import time
import random
import csv 

from abb import insert as abb_insert, search as abb_search, delete as abb_delete, height as abb_height
import avl
from hash_open import OpenAddressHashTable
from hash_chaining import HashTableChaining

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

    def insert(self, key: int) -> None:
        self.root = abb_insert(self.root, key)

    def search(self, key: int) -> bool:
        return abb_search(self.root, key) is not None

    def delete(self, key: int) -> None:
        self.root = abb_delete(self.root, key)

    def extra_metrics(self) -> dict:
        return {
            "altura_final": abb_height(self.root),
        }


class AVLWrapper:

    def __init__(self):
        self.root = None
        if hasattr(avl, "reset_rotation_count"):
            avl.reset_rotation_count()

    def insert(self, key: int) -> None:
        self.root = avl.insert(self.root, key)

    def search(self, key: int) -> bool:
        return avl.search(self.root, key) is not None

    def delete(self, key: int) -> None:
        self.root = avl.delete(self.root, key)

    def extra_metrics(self) -> dict:
        metrics = {
            "altura_final": avl.height(self.root),
        }
        if hasattr(avl, "get_rotation_count"):
            metrics["rotacoes"] = avl.get_rotation_count()
        return metrics


class HashOpenWrapper:

    def __init__(self, size: int, method: str):
        self.table = OpenAddressHashTable(size=size, method=method)

    def insert(self, key: int) -> None:
        self.table.insert(key)

    def search(self, key: int) -> bool:
        return self.table.search(key)

    def delete(self, key: int) -> None:
        self.table.remove(key)

    def extra_metrics(self) -> dict:
        return {
            "tamanho_tabela": self.table.size,
            "fator_de_carga": round(self.table.load_factor(), 3),
            "colisoes_totais": self.table.collision_count,
        }


class HashChainingWrapper:

    def __init__(self, size: int):
        self.table = HashTableChaining(size=size, debug=False)

    def insert(self, key: int) -> None:
        self.table.insert(key)

    def search(self, key: int) -> bool:
        return self.table.search(key)

    def delete(self, key: int) -> None:
        self.table.remove(key)

    def extra_metrics(self) -> dict:
        return {
            "tamanho_tabela": self.table.size,
            "colisoes_totais": self.table.collision_count,
        }


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

    resultado = {
        "estrutura": nome_estrutura,
        "tempo_medio_insercao": tempo_insercao_medio,
        "tempo_medio_busca": tempo_busca_medio,
        "tempo_medio_remocao": tempo_remocao_medio,
    }
    resultado.update(estrutura.extra_metrics())
    return resultado


def imprimir_resultado(r: dict) -> None:
    """Imprime as métricas na tela, como já fazia antes."""
    print(f"\nEstrutura: {r['estrutura']}")
    print(f"  Tempo médio inserção: {r['tempo_medio_insercao']:.6e} s")
    print(f"  Tempo médio busca   : {r['tempo_medio_busca']:.6e} s")
    print(f"  Tempo médio remoção : {r['tempo_medio_remocao']:.6e} s")

    if "altura_final" in r:
        print(f"  Altura final        : {r['altura_final']}")
    if "rotacoes" in r:
        print(f"  Rotações            : {r['rotacoes']}")
    if "tamanho_tabela" in r:
        print(f"  Tamanho da tabela   : {r['tamanho_tabela']}")
    if "fator_de_carga" in r:
        print(f"  Fator de carga      : {r['fator_de_carga']}")
    if "colisoes_totais" in r:
        print(f"  Colisões totais     : {r['colisoes_totais']}")
    print()


def salvar_resultados_csv(resultados: list, caminho: str) -> None:
    fieldnames = [
        "dataset",
        "estrutura",
        "N",
        "M",
        "K",
        "tempo_medio_insercao",
        "tempo_medio_busca",
        "tempo_medio_remocao",
        "altura_final",
        "rotacoes",
        "tamanho_tabela",
        "fator_de_carga",
        "colisoes_totais",
    ]

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in resultados:
            writer.writerow(r)

    print(f"\nResultados salvos em: {caminho}")



def main():
    N = 25_000   #MUDAR AQ O VALOR PARA TESTAR
    M = N
    K = N // 10
    random.seed(42)

    tamanho_tabela_hash = N * 2  

    datasets = {
        "aleatorio": gerar_aleatorio(N),
        "ordenado": gerar_ordenado(N),
        "quase_ordenado": gerar_quase_ordenado(N),
    }

    estruturas_arvores = {
        "ABB": lambda: ABBWrapper(),
        "AVL": lambda: AVLWrapper(),
    }

    resultados_csv = []

    for nome_dataset, chaves in datasets.items():
        print("\n====================================")
        print(f"DATASET: {nome_dataset}  (N={N}, M={M}, K={K})")
        print("====================================")

        for nome_estrutura, fabrica in estruturas_arvores.items():
            r = executar_benchmark_estrutura(
                nome_estrutura=nome_estrutura,
                fabrica=fabrica,
                chaves_base=chaves,
                m=M,
                k=K,
            )
            imprimir_resultado(r)

            resultados_csv.append({
                "dataset": nome_dataset,
                "estrutura": r["estrutura"],
                "N": N,
                "M": M,
                "K": K,
                "tempo_medio_insercao": r["tempo_medio_insercao"],
                "tempo_medio_busca": r["tempo_medio_busca"],
                "tempo_medio_remocao": r["tempo_medio_remocao"],
                "altura_final": r.get("altura_final", ""),
                "rotacoes": r.get("rotacoes", ""),
                "tamanho_tabela": r.get("tamanho_tabela", ""),
                "fator_de_carga": r.get("fator_de_carga", ""),
                "colisoes_totais": r.get("colisoes_totais", ""),
            })

        r = executar_benchmark_estrutura(
            nome_estrutura="Hash (encadeamento externo)",
            fabrica=lambda: HashChainingWrapper(size=tamanho_tabela_hash),
            chaves_base=chaves,
            m=M,
            k=K,
        )
        imprimir_resultado(r)
        resultados_csv.append({
            "dataset": nome_dataset,
            "estrutura": r["estrutura"],
            "N": N,
            "M": M,
            "K": K,
            "tempo_medio_insercao": r["tempo_medio_insercao"],
            "tempo_medio_busca": r["tempo_medio_busca"],
            "tempo_medio_remocao": r["tempo_medio_remocao"],
            "altura_final": "",
            "rotacoes": "",
            "tamanho_tabela": r.get("tamanho_tabela", ""),
            "fator_de_carga": "",
            "colisoes_totais": r.get("colisoes_totais", ""),
        })

        for metodo in ("linear", "quadratic", "double"):
            r = executar_benchmark_estrutura(
                nome_estrutura=f"Hash (open addressing, {metodo})",
                fabrica=lambda m=metodo: HashOpenWrapper(
                    size=tamanho_tabela_hash,
                    method=m,
                ),
                chaves_base=chaves,
                m=M,
                k=K,
            )
            imprimir_resultado(r)
            resultados_csv.append({
                "dataset": nome_dataset,
                "estrutura": r["estrutura"],
                "N": N,
                "M": M,
                "K": K,
                "tempo_medio_insercao": r["tempo_medio_insercao"],
                "tempo_medio_busca": r["tempo_medio_busca"],
                "tempo_medio_remocao": r["tempo_medio_remocao"],
                "altura_final": "",
                "rotacoes": "",
                "tamanho_tabela": r.get("tamanho_tabela", ""),
                "fator_de_carga": r.get("fator_de_carga", ""),
                "colisoes_totais": r.get("colisoes_totais", ""),
            })

    salvar_resultados_csv(resultados_csv, "resultados_benchmark.csv")


if __name__ == "__main__":
    main()
