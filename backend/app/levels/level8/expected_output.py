import networkx as nx


def readGraph(file):
    try:
        nx.read_graphml(file)
    except FileExistsError:
        return nx.Graph()


n = int(input())


def dfs(startowy, G):
    vis = set()
    stos = []

    stos.append(startowy)

    while len(stos):
        aktualny = stos.pop()

        if aktualny in vis:
            continue
        vis.add(aktualny)

        for sasiad in G.neighbors(aktualny):
            stos.append(sasiad)
