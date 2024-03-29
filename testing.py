import networkx as nx
from networkx import square_clustering, clustering, triangles
from networkx import degree_centrality, closeness_centrality, pagerank, betweenness_centrality, eigenvector_centrality
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

def triangle_strategy(G, seed):
    scores = triangles(G)
    centrality = [(scores[node], node) for node in scores]
    nlargest = heapq.nlargest(seed, centrality)
    strategy = [node for (_, node) in nlargest]
    return strategy

def combine_cluster_centrality(G, seed, c_type):
    clust_strat = set(triangle_strategy(G, seed))
    centrality_strat = set(centrality_strategy(G, seed, c_type))
    mixed_strat = clust_strat.intersection(centrality_strat)
    centrality_leftover = centrality_strat.difference(mixed_strat)
    clust_leftover = clust_strat.difference(mixed_strat)
    if len(mixed_strat) < seed:
        while len(mixed_strat) < seed:
            coin_flip = random.random()
            node = None
            if coin_flip < 0.5:
                node = random.choice(list(centrality_leftover))
                centrality_leftover.remove(node)
            else:
                node = random.choice(list(clust_leftover))
                clust_leftover.remove(node)
            mixed_strat.add(node)
    return list(mixed_strat)

def output_to_submission(graph_file, strategy, strategy_name):
    output_file = 'submissions/' + ''.join(graph_file.split('.')[:3]) + strategy_name + '.txt'
    strategy_string = ''
    for _ in range(50):
        for node in strategy:
            strategy_string += node + '\n'
    f = open(output_file, 'w')
    f.write(strategy_string)
    f.close()

def centrality_strategy(G, seed, c_type):
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
    return strategy

def max_neighbors_strat(G, seed):
    degrees = closeness_centrality(G)
    highest_degree_node = max(degrees, key = degrees.get)
    neighbors = nx.neighbors(G, highest_degree_node)
    neighbor_degrees = [(degrees[node], node) for node in neighbors]
    nlargest = heapq.nlargest(seed-1, neighbor_degrees)
    strat = [node for (_,node) in nlargest]
    strat.append(highest_degree_node)
    return strat

def max_neighbors_strat2(G, seed):
    degrees = closeness_centrality(G)
    degrees_sorted = sorted([(degrees[node], node) for node in degrees], reverse=True)
    max2 = [u for (_,u) in degrees_sorted[:2]]
    strat = []
    for node in max2:
        neighbors = nx.neighbors(G, node)
        neighbor_degrees = [(degrees[u], u) for u in neighbors]
        nlargest = heapq.nlargest((seed-2)//2, neighbor_degrees)
        for _,u in nlargest:
            strat.append(u)
        strat.append(node)
    return strat

if __name__ == '__main__':
    for file in os.listdir(GRAPH_DIR):
        graph_file = os.path.join(GRAPH_DIR, file)
        if not os.path.isfile(graph_file):
            raise Exception('Not a file!')
        G, seed, adj_list = read_graph(graph_file)
        #output_strategy(G, seed, graph_file)
        cent_types = ['closeness', 'betweeness', 'degree', 'eigenvector']
        # clust_types = ['square', 'clustering', 'triangle']
        measures = cent_types
        max_score, best_measure = float('-INF'), None
        strategy_dict = {}
        ta_hard = max_neighbors_strat(G, seed)
        strategy_dict['ta_hard'] = ta_hard
        print(f'{file}:')
        for a in measures:
            strategy_dict['nlargest'] = centrality_strategy(G, seed, a)
            result = sim.run(adj_list, strategy_dict)
            print(f'{a}:')
            print(result)
            continue
            for b in measures:
                if a != b:
                    strategy_dict = {}
                    strategy_dict[a] = combine_cluster_centrality(G, seed, a)
                    strategy_dict[b] = combine_cluster_centrality(G, seed, b)
                    result = sim.run(adj_list, strategy_dict)
                    print(file, result)
                    new_max = max(list(result.values()))
                    if new_max > max_score:
                        best_measure = max(result, key=result.get)
                        max_score = new_max

        #print(f'{best_measure} clustering wins for {file} with {max_score} nodes')
        #print(f'That is {max_score*100/len(G.nodes)}% of the graph')
        #print('---------------------------')
