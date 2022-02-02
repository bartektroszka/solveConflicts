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

    while not stos.empty():
        x = stos.pop()

        if x in vis:
            continue
        vis.add(x)

        for sasiad in G.neighbors(x):
            stos.push(sasiad)
