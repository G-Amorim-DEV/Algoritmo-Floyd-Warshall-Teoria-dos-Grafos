import networkx as nx
import matplotlib.pyplot as plt

def criar_grafo(matriz):

    G = nx.DiGraph()

    n = len(matriz)

    for i in range(n):
        for j in range(n):

            if matriz[i][j] != 9999 and i != j:

                G.add_edge(i, j, weight=matriz[i][j])

    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # return the current figure instead of showing it directly so callers can display it as needed
    return plt.gcf()

