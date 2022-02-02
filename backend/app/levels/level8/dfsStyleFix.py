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
    vis.add(startowy)

    while len(stos):
        aktualny = stos.pop()
        for sasiad in G.neighbors(aktualny):
            if sasiad not in vis:
                vis.add(sasiad)
                stos.append(sasiad)
