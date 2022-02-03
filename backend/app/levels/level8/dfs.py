import networkx as nx


def readGraph():
    try:
        nx.read_graphml('graf.graphml')
    except FileExistsError:
        return nx.Graph()


n = int(input())


def dfs(w, G):
    vis = set()
    stos = []

    stos.append(w)
    vis.add(w)

    while len(stos):
        x = stos.pop()
        for sasiad in G.neighbors(x):
            if sasiad not in vis:
                vis.add(sasiad)
                stos.append(sasiad)
