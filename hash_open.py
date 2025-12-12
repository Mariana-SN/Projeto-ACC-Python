import time
import random

class DeletedEntry:
    pass

DELETED = DeletedEntry()

class OpenAddressHashTable:
    def __init__(self, size=11, method="linear"):
        self.size = size
        self.table = [None] * size
        self.count = 0

        assert method in ["linear", "quadratic", "double"]
        self.method = method

        self.collision_count = 0
        self.insert_times = []
        self.search_times = []
        self.remove_times = []

    def load_factor(self):
        return self.count / self.size

    def hash1(self, key):
        return hash(key) % self.size

    def hash2(self, key):
        return 1 + (hash(key) % (self.size - 1))

    def _probe(self, key, i):
        if self.method == "linear":
            return (self.hash1(key) + i) % self.size

        elif self.method == "quadratic":
            return (self.hash1(key) + i * i) % self.size

        elif self.method == "double":
            return (self.hash1(key) + i * self.hash2(key)) % self.size

    def insert(self, key):
        start = time.perf_counter()

        if self.count == self.size:
            raise Exception("Tabela cheia")

        for i in range(self.size):
            index = self._probe(key, i)

            if self.table[index] is None or self.table[index] is DELETED:
                self.table[index] = key
                self.count += 1
                self.insert_times.append(time.perf_counter() - start)
                return True

            self.collision_count += 1

        self.insert_times.append(time.perf_counter() - start)
        return False

    def search(self, key):
        start = time.perf_counter()

        for i in range(self.size):
            index = self._probe(key, i)

            if self.table[index] is None:
                self.search_times.append(time.perf_counter() - start)
                return False

            if self.table[index] == key:
                self.search_times.append(time.perf_counter() - start)
                return True

        self.search_times.append(time.perf_counter() - start)
        return False

    def remove(self, key):
        start = time.perf_counter()

        for i in range(self.size):
            index = self._probe(key, i)

            if self.table[index] is None:
                self.remove_times.append(time.perf_counter() - start)
                return False

            if self.table[index] == key:
                self.table[index] = DELETED
                self.count -= 1
                self.remove_times.append(time.perf_counter() - start)
                return True

        self.remove_times.append(time.perf_counter() - start)
        return False

    def report(self):
        def avg(lst):
            return sum(lst) / len(lst) if lst else 0

        return {
            f"tamanho_tabela": self.size,
            f"fator_de_carga": round(self.load_factor(), 3),
            f"colisoes_totais": self.collision_count,
            f"tempo_medio_insercao": avg(self.insert_times),
            f"tempo_medio_busca": avg(self.search_times),
            f"tempo_medio_remocao": avg(self.remove_times),
        }

    def print_table(self):
        print("Tabela Hash:")
        for i, item in enumerate(self.table):
            if item is None:
                print(f"{i}: vazio")
            elif item is DELETED:
                print(f"{i}: <removido>")
            else:
                print(f"{i}: {item}")


def benchmark_open_addressing(size=1000, operations=500, method="", seed=42):
    random.seed(seed)
    table = OpenAddressHashTable(size=size, method=method)

    print("Benchmark da Tabela Hash (Open Addressing):")
    print(f"Método: {method}")
    print(f"Tamanho da tabela: {size}")
    print(f"Operações: {operations}")

    keys = random.sample(range(size * 10), operations)

    for key in keys:
        try:
            table.insert(key)
        except Exception:
            break 

    search_keys = random.sample(keys, operations // 2)
    for key in search_keys:
        table.search(key)

    removal_keys = random.sample(keys, operations // 4)
    for key in removal_keys:
        table.remove(key)

    report = table.report()

    print("\nResultados do Benchmark")
    print(f"Método:                {method}")
    print(f"Tamanho da tabela:     {report['tamanho_tabela']}")
    print(f"Fator de carga final:  {report['fator_de_carga']}")
    print(f"Colisões totais:       {report['colisoes_totais']}")
    print(f"Tempo médio inserção:  {report['tempo_medio_insercao']:.8f} s")
    print(f"Tempo médio busca:     {report['tempo_medio_busca']:.8f} s")
    print(f"Tempo médio remoção:   {report['tempo_medio_remocao']:.8f} s")

    return report

def print_report(report):
    print("\nRelatório:")
    print(f"Tamanho da tabela:     {report['tamanho_tabela']}")
    print(f"Fator de carga:        {report['fator_de_carga']}")
    print(f"Colisões totais:       {report['colisoes_totais']}")
    print(f"Tempo médio inserção:  {report['tempo_medio_insercao']:.8f} s")
    print(f"Tempo médio busca:     {report['tempo_medio_busca']:.8f} s")
    print(f"Tempo médio remoção:   {report['tempo_medio_remocao']:.8f} s")

if __name__ == "__main__":
    h = OpenAddressHashTable(size=11, method="double")

    h.insert(10)
    h.insert(21)
    h.insert(32)
    h.insert(43)
    h.insert(54)

    h.print_table()
    print("\n")

    print("Busca 21:", h.search(21))
    print("Remove 32:", h.remove(32))
    print("\n")

    h.print_table()
    print("\n")

    print_report(h.report())
    print("\n")

    # COM BENCHMARK PROVISÓRIO!!! UNIFICAR E ALTERAR LÓGICA PARA FUNCIONAR NO ARQUIVO BENCHMARK.PY 

    print("Benchmark:")

    methods = ["linear", "quadratic", "double"]

    for m in methods:
        print(f"\nExecutando benchmark para método: {m}")
        benchmark_open_addressing(
            size=2000,
            operations=1000,
            method=m
        )