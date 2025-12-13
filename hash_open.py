import time

class DeletedEntry:
    pass

DELETED = DeletedEntry()

class OpenAddressHashTable:
    def __init__(self, size=11, method="linear", debug=False):
        self.size = size
        self.table = [None] * size
        self.count = 0

        assert method in ["linear", "quadratic", "double"]
        self.method = method

        self.collision_count = 0
        self.insert_times = []
        self.search_times = []
        self.remove_times = []

        self.debug = debug

    def _log(self, msg: str):
        if self.debug:
            print(msg)

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

        self._log(f"\n[INSERIR] Quero inserir a chave {key}")
        self._log(f"Hash primário: {self.hash1(key)}")
        if self.method == "double":
            self._log(f"Hash secundário: {self.hash2(key)}")

        for i in range(self.size):
            index = self._probe(key, i)
            self._log(f"Tentativa {i}: posição {index}")

            if self.table[index] is None:
                self._log("Posição vazia encontrada")
                self.table[index] = key
                self.count += 1
                self.insert_times.append(time.perf_counter() - start)
                return True

            if self.table[index] is DELETED:
                self._log("Posição marcada como REMOVIDA")
                self.table[index] = key
                self.count += 1
                self.insert_times.append(time.perf_counter() - start)
                return True

            self.collision_count += 1
            self._log(f"Colisão! Já existe {self.table[index]} nessa posição")

        self._log("Falha ao inserir: tabela cheia após sondagens")
        self.insert_times.append(time.perf_counter() - start)
        return False

    def search(self, key):
        start = time.perf_counter()

        self._log(f"\n[BUSCAR] Procurando a chave {key}")

        for i in range(self.size):
            index = self._probe(key, i)
            self._log(f"Tentativa {i}: posição {index}")

            if self.table[index] is None:
                self._log("Posição vazia, chave não está na tabela")
                self.search_times.append(time.perf_counter() - start)
                return False

            if self.table[index] == key:
                self._log("Chave encontrada")
                self.search_times.append(time.perf_counter() - start)
                return True

            self._log(f"Elemento diferente encontrado ({self.table[index]}), continuando sondagem")

        self._log("Chave não encontrada após todas as sondagens")
        self.search_times.append(time.perf_counter() - start)
        return False

    def remove(self, key):
        start = time.perf_counter()

        self._log(f"\n[REMOVER] Tentando remover a chave {key}")

        for i in range(self.size):
            index = self._probe(key, i)
            self._log(f"Tentativa {i}: posição {index}")

            if self.table[index] is None:
                self._log("Posição vazia, chave não existe")
                self.remove_times.append(time.perf_counter() - start)
                return False

            if self.table[index] == key:
                self._log("Chave encontrada, marcando como removida")
                self.table[index] = DELETED
                self.count -= 1
                self.remove_times.append(time.perf_counter() - start)
                return True

            self._log(f"Elemento diferente ({self.table[index]}), continuando sondagem")

        self._log("Chave não encontrada após todas as sondagens")
        self.remove_times.append(time.perf_counter() - start)
        return False

    def report(self):
        def avg(lst):
            return sum(lst) / len(lst) if lst else 0.0

        return {
            f"tamanho_tabela": self.size,
            f"fator_de_carga": round(self.load_factor(), 3),
            f"colisoes_totais": self.collision_count,
            f"tempo_medio_insercao": avg(self.insert_times),
            f"tempo_medio_busca": avg(self.search_times),
            f"tempo_medio_remocao": avg(self.remove_times),
        }

    def print_table(self):
        print("\nTabela Hash (Enderecamento aberto):")
        for i, item in enumerate(self.table):
            if item is None:
                print(f"{i}: vazio")
            elif item is DELETED:
                print(f"{i}: <removido>")
            else:
                print(f"{i}: {item}")

def print_report(report):
        print("\nMetricas da tabela Hash (Enderecamento aberto):")
        print(f"Tamanho da tabela:     {report['tamanho_tabela']}")
        print(f"Fator de carga:        {report['fator_de_carga']}")
        print(f"Colisões totais:       {report['colisoes_totais']}")
        print(f"Tempo médio inserção:  {report['tempo_medio_insercao']:.8f} s")
        print(f"Tempo médio busca:     {report['tempo_medio_busca']:.8f} s")
        print(f"Tempo médio remoção:   {report['tempo_medio_remocao']:.8f} s")

if __name__ == "__main__":
    h = OpenAddressHashTable(size=7, method="double", debug=True)

    h.insert(10)
    h.insert(17)
    h.insert(21)
    h.insert(32)
    h.insert(43)
    h.insert(54)

    print("\nTabela após inserções:")
    h.print_table()

    h.search(21)
    h.search(99)

    print("\nTabela após remoção de 24:")
    h.remove(32)

    h.print_table()
    print()

    print_report(h.report())