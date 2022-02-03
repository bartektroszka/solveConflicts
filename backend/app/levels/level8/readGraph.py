import networkx as nx


def readGraph(file):
    return nx.read_graphml(file)
