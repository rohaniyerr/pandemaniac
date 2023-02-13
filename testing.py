import networkx as nx
from networkx import average_clustering, clustering, triangles
from networkx import degree_centrality, closeness_centrality, betweenness_centrality
import json
import random
import sim
import matplotlib.pyplot as plt
import heapq

graph_file = 'RR.10.50.json'

def read_graph(graph_file):
    G = nx.Graph()
    with open('graphs/' + graph_file) as jsonfile:
        adj_list = json.load(jsonfile)
        for i in adj_list:
            G.add_node(i)
            for j in adj_list[i]:
                G.add_edge(i,j)
    x = graph_file.split('.')
    seed = int(x[1])
    return G, seed, adj_list

def random_nodes(G, seed):
    nodes = list(G.nodes)
    return random.sample(nodes, seed)

def output_random_strategy(G, seed, graph_file):
    output_file = 'submissions/' + ''.join(graph_file.split('.')[:3]) + '.txt'
    strategy = ''
    for _ in range(50):
        nodes = random_nodes(G, seed)
        for node in nodes:
            strategy += str(node) + '\n'
    f = open(output_file, 'w')
    f.write(strategy)
    f.close()

def centrality_strategy(G, seed, graph_file, c_type):
    c_scores = None
    if c_type == 'closeness':
        c_scores = closeness_centrality(G)
    elif c_type == 'degree':
        c_scores = degree_centrality(G)
    elif c_type == 'betweeness':
        c_scores = betweenness_centrality(G)
    else:
        return None
    centrality = [(c_scores[node], node) for node in c_scores]
    nlargest = heapq.nlargest(seed, centrality)
    strategy = [node for (_, node) in nlargest]
    output_file = 'submissions/' + ''.join(graph_file.split('.')[:3]) + c_type + '.txt'
    strategy_string = ('\n'.join(strategy) + '\n') * seed
    f = open(output_file, 'w')
    f.write(strategy_string)
    f.close()
    return strategy

if __name__ == '__main__':
    G, seed, adj_list = read_graph(graph_file)
    #output_strategy(G, seed, graph_file)
    ctypes = ['closeness', 'degree', 'betweeness']
    for a in ctypes:
        for b in ctypes:
            if a != b:
                strategy_dict = {}
                strategy_dict[a] = centrality_strategy(G, seed, graph_file, a)
                strategy_dict[b] = centrality_strategy(G, seed, graph_file, b)
                result = sim.run(adj_list, strategy_dict)
                print(result)
