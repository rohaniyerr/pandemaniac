import networkx as nx
from networkx import average_clustering, clustering, triangles
from networkx import degree_centrality, closeness_centrality, betweenness_centrality
import numpy as np
import json

def read_graph(graph_file):
    adj_list = json.loads(graph_file)
    G = nx.Graph()
    for i in adj_list:
        G.add_node(int(i))
        for j in adj_list[i]:
            G.add_edge(int(i),int(j))
    seed = int(graph_file.split('.')[1])
    return G, seed

def random_nodes(G, seed):
    pass

def output_strategy(G, seed, graph_file):
    output_file = graph_file.split('.')[:2] + '.txt'
    strategy = ''
    for _ in range(50):
        nodes = random_nodes(G, seed)
        for node in nodes:
            strategy += node + '\n'
    f = open(output_file, 'w')
    f.write(strategy)
    f.close()

