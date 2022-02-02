import networkx as nx


def readGraph(file):
    try:
        nx.read_graphml(file)
    except FileExistsError:
        return nx.Graph()


n = int(input())
