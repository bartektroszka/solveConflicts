import networkx as nx


def readGraph(file):
    try:
        nx.read_graphml(file)
    except FileExistsError:
        return nx.Graph()


n = int(input())


def dfs(w, G):
    vis = set()
    stos = []

    stos.append(w)

    while len(stos):
        x = stos.pop()

        if x in vis:
            continue
        vis.add(x)

        for sasiad in G.neighbors(x):
            stos.append(sasiad)
