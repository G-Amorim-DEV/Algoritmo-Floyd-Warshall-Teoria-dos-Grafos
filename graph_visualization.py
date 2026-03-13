import networkx as nx
import matplotlib.pyplot as plt

def criar_grafo(matriz):
    G = nx.DiGraph()
    n = len(matriz)

    for i in range(n):
        for j in range(n):
            # Substituído 9999 por float('inf')
            if i != j and matriz[i][j] != float('inf'):
                G.add_edge(i, j, weight=matriz[i][j])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6)) # Define um tamanho padrão para o Streamlit
    
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            node_size=700, font_size=12, font_weight='bold')

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    return plt.gcf()