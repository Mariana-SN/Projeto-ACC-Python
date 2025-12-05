
import random


def gerar_aleatorio(n, minimo=1, maximo=1_000_000_000):
    return random.sample(range(minimo, maximo), n)


def gerar_ordenado(n, minimo=1, maximo=1_000_000_000):
    chaves = gerar_aleatorio(n, minimo, maximo)
    chaves.sort()
    return chaves


def gerar_quase_ordenado(
    n,
    minimo=1,
    maximo=1_000_000_000,
    porcentagem_bagunca=0.10,
):
 
    chaves = gerar_ordenado(n, minimo, maximo)
    qtd_bagunca = int(n * porcentagem_bagunca)

    indices = random.sample(range(n), qtd_bagunca)
    sublista = [chaves[i] for i in indices]
    random.shuffle(sublista)

    for idx, valor in zip(indices, sublista):
        chaves[idx] = valor

    return chaves


def montar_chaves_busca(
    chaves_inseridas,
    m,
    minimo=1,
    maximo=1_000_000_000,
):

    m_presentes = m // 2
    presentes = random.sample(chaves_inseridas, min(m_presentes, len(chaves_inseridas)))

    conjunto = set(chaves_inseridas)
    ausentes = []

    while len(ausentes) < m - len(presentes):
        candidato = random.randint(minimo, maximo)
        if candidato not in conjunto:
            ausentes.append(candidato)

    return presentes + ausentes
