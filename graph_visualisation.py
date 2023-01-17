import networkx as nx
import numpy as np
import matplotlib.pyplot as plt 
from src.classes import Graph
from networkx.drawing.nx_agraph import graphviz_layout
    
def graph_visualise(g):
    plt.close('all')
    # Create an empty graph
    G = nx.Graph()
    
    g = g.matrix
    
    new_g = np.zeros(shape=(len(g)+1, len(g[0]) + 1))

    for i in range(1, len(new_g)):
        for j in range(1, len(new_g[0])):
            if i == j:
                new_g[0][j] = g[i-1][j-1]
                new_g[i][0] = g[i-1][j-1]
            else:
                new_g[i][j] = g[i-1][j-1]

    # Add the edges to the graph with the corresponding labels
    for i, row in enumerate(new_g):
        for j, val in enumerate(row):
            if val != 0:
                G.add_edge(i, j, weight=int(val))

    # Get the edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    labels = {}
    for i in range(len(g)+1):
        labels[i] = str(i)
    labels[0] = "Refill"
    
    plt.figure()
    # Draw the graph using circular layout
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos, labels)
    plt.show()