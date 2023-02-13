import networkx as nx
from networkx import square_clustering, clustering, triangles
from networkx import degree_centrality, closeness_centrality, betweenness_centrality, eigenvector_centrality
import json
import random
import sim
import matplotlib.pyplot as plt
import heapq
import os

GRAPH_DIR = 'graphs'
graph_file = 'RR.10.50.json'
RUN_ALL_GRAPHS = True

def read_graph(graph_file):
    G = nx.Graph()
    with open(graph_file) as jsonfile:
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


def clustering_strategy(G, measure):
    scores = None
    if measure == 'square':
        scores = square_clustering(G)
    elif measure == 'clustering':
        scores = clustering(G)
    elif measure == 'triangle':
        scores = triangles(G)
    else:
        return None
    centrality = [(scores[node], node) for node in scores]
    nlargest = heapq.nlargest(seed, centrality)
    strategy = [node for (_, node) in nlargest]
    return strategy



def centrality_strategy(G, seed, graph_file, c_type):
    c_scores = None
    if c_type == 'closeness':
        c_scores = closeness_centrality(G)
    elif c_type == 'degree':
        c_scores = degree_centrality(G)
    elif c_type == 'betweeness':
        c_scores = betweenness_centrality(G)
    elif c_type == 'eigenvector':
        c_scores = eigenvector_centrality(G)
    else:
        return None
    
    centrality = [(c_scores[node], node) for node in c_scores]
    nlargest = heapq.nlargest(seed, centrality)
    strategy = [node for (_, node) in nlargest]
    if not RUN_ALL_GRAPHS:
        output_file = 'submissions/' + ''.join(graph_file.split('.')[:3]) + c_type + '.txt'
        strategy_string = ('\n'.join(strategy) + '\n') * seed
        f = open(output_file, 'w')
        f.write(strategy_string)
        f.close()
    return strategy

if __name__ == '__main__':
    for file in os.listdir(GRAPH_DIR):
        graph_file = os.path.join(GRAPH_DIR, file)
        if not os.path.isfile(graph_file):
            raise Exception('Not a file!')
        G, seed, adj_list = read_graph(graph_file)
        #output_strategy(G, seed, graph_file)
        cent_types = ['closeness', 'betweeness', 'degree', 'eigenvector']
        clust_types = ['square', 'clustering', 'triangle']

        measures = clust_types

        max_score, best_measure = float('-INF'), None
        for a in measures:
            for b in measures:
                if a != b:
                    strategy_dict = {}
                    strategy_dict[a] = clustering_strategy(G, a)
                    strategy_dict[b] = clustering_strategy(G, b)
                    result = sim.run(adj_list, strategy_dict)
                    print(file, result)
                    new_max = max(list(result.values()))
                    if new_max > max_score:
                        best_measure = max(result, key=result.get)
                        max_score = new_max

        print(f'{best_measure} clustering wins for {file} with {max_score} nodes')
        print(f'That is {max_score*100/len(G.nodes)}% of the graph')
        print('---------------------------')

