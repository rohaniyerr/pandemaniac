import networkx as nx
from networkx import average_clustering, clustering, triangles
from networkx import degree_centrality, closeness_centrality, betweenness_centrality
import numpy as np
import json
import random

graph_file = 'graphs/RR.5.10.json'

def read_graph(graph_file):
    G = nx.Graph()
    with open(graph_file) as jsonfile:
        adj_list = json.load(jsonfile)
        for i in adj_list:
            G.add_node(int(i))
            for j in adj_list[i]:
                G.add_edge(int(i),int(j))
    x = graph_file.split('.')
    seed = int(x[1])
    graph_type = int(x[2])
    return G, seed, graph_type

def random_nodes(G, seed):
    nodes = list(G.nodes)
    return random.sample(nodes, seed)

def output_strategy(G, seed, graph_file):
    output_file = 'submissions' + ''.join(graph_file.split('.')[:3]) + '.txt'
    strategy = ''
    for _ in range(50):
        nodes = random_nodes(G, seed)
        for node in nodes:
            strategy += str(node) + '\n'
    f = open(output_file, 'w')
    f.write(strategy)
    f.close()

if __name__ == '__main__':
    G, seed, graph_type = read_graph(graph_file)
    output_strategy(G, seed, graph_file)
