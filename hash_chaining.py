import time

class HashTableChaining:
    def __init__(self, size=11, debug=False):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

        self.collision_count = 0
        self.insert_times = []
        self.search_times = []
        self.remove_times = []

        self.debug = debug

    def _log(self, msg: str):
        if self.debug:
            print(msg)

    def _hash(self, key):
        return hash(key) % self.size

    def load_factor(self):
        if self.size == 0:
            return 0.0
        return self.count / self.size

    def insert(self, key):
        start = time.perf_counter()

        index = self._hash(key)
        bucket = self.table[index]

        self._log(f"[INSERIR] Quero guardar a chave {key}")
        self._log(f"Ela caiu na posição {index} da tabela")
        self._log(f"Conteúdo dessa posição ANTES: {bucket}")

        for existing in bucket:
            if existing == key:
                self._log("Essa chave já estava na tabela")
                self.insert_times.append(time.perf_counter() - start)
                return False

        if bucket:
            self.collision_count += 1
            self._log("Já tinha chave nessa posição, ocorre uma colisão")

        bucket.append(key)
        self.count += 1

        self.insert_times.append(time.perf_counter() - start)

        self._log(f"Valor dessa posição DEPOIS: {bucket}")
        return True

    def search(self, key):
        start = time.perf_counter()

        index = self._hash(key)
        bucket = self.table[index]

        self._log(f"[BUSCAR] Quero saber se a chave {key} está na tabela.")
        self._log(f"Ela deveria estar na posição {index}.")
        self._log(f"Conteúdo dessa posição: {bucket}")

        for element in bucket:
            self._log(f"Comparando com {element}...")
            if element == key:
                self.search_times.append(time.perf_counter() - start)
                self._log("Chave encontrada nessa posição.")
                return True

        self.search_times.append(time.perf_counter() - start)
        self._log("Chave não encontrada na tabela.")
        return False

    def remove(self, key):
        start = time.perf_counter()

        index = self._hash(key)
        bucket = self.table[index]

        self._log(f"[REMOVER] Quero remover a chave {key}.")
        self._log(f"Espera-se que esteja na posição {index}.")
        self._log(f"Conteúdo da posição antes: {bucket}")

        for i, element in enumerate(bucket):
            self._log(f"Comparando com {element}...")
            if element == key:
                del bucket[i]
                self.count -= 1
                self.remove_times.append(time.perf_counter() - start)
                self._log("Chave encontrada e removida.")
                self._log(f"Conteúdo dessa posição DEPOIS: {bucket}")
                return True

        self.remove_times.append(time.perf_counter() - start)
        self._log("Chave não encontrada, nada foi removido.")
        return False

    def report(self):
        def avg(lst):
            return sum(lst) / len(lst) if lst else 0.0

        return {
            "tamanho_tabela": self.size,
            "colisoes_totais": self.collision_count,
            "tempo_medio_insercao": avg(self.insert_times),
            "tempo_medio_busca": avg(self.search_times),
            "tempo_medio_remocao": avg(self.remove_times),
        }

    def print_table(self):
        print("Tabela Hash (encadeamento externo):")
        for i, bucket in enumerate(self.table):
            if not bucket:
                print(f"{i}: vazio")
            else:
                print(f"{i}: {bucket}")


def print_report(report):
    print("\nResumo das métricas da tabela (encadeamento externo):")
    print(f"Tamanho da tabela:     {report['tamanho_tabela']}")
    print(f"Colisões totais:       {report['colisoes_totais']}")
    print(f"Tempo médio inserção:  {report['tempo_medio_insercao']:.8f} s")
    print(f"Tempo médio busca:     {report['tempo_medio_busca']:.8f} s")
    print(f"Tempo médio remoção:   {report['tempo_medio_remocao']:.8f} s")


if __name__ == "__main__":
    h = HashTableChaining(size=7, debug=True)

    h.insert(10)
    h.insert(17)
    h.insert(24)
    h.insert(31)
    h.insert(4)

    print("\nTabela após inserções:")
    h.print_table()
    print()

    h.search(17)
    h.search(99)

    h.remove(24)

    print("\nTabela após remoção de 24:")
    h.print_table()
    print()

    print_report(h.report())
