import networkx as nx
from networkx import square_clustering, clustering, triangles
from networkx import degree_centrality, closeness_centrality, betweenness_centrality, eigenvector_centrality
from networkx.algorithms.community import greedy_modularity_communities

import json
import random
import sim
import matplotlib.pyplot as plt
import heapq
from sklearn.cluster import KMeans, SpectralClustering
import os
import testing
from collections import defaultdict

GRAPH_DIR = 'graphs'
RUN_ALL_GRAPHS = False
SINGLE_GRAPH = 'J.5.10.json'

#all of these suck
def dominating_strategy(G, seed):
    centrality_measure = nx.betweenness_centrality(G)
    highest_degree_node = max(centrality_measure, key=centrality_measure.get)
    dominating_set = nx.dominating_set(G, start_with=highest_degree_node)
    degrees = {node:degree for node, degree in centrality_measure.items() if node in dominating_set}
    nlargest = heapq.nlargest(seed, [(degree, node) for node, degree in degrees.items()])
    strategy = [node for (_,node) in nlargest]
    return strategy

def clique_strategy(G, seed):
    cliques = greedy_modularity_communities(G, n_communities=seed)
    centrality_measure = nx.degree_centrality(G)
    highest_degree_representatives = {}
    for clique in cliques:
        max_degree, rep = float('-INF'), None
        for node in clique:
            if centrality_measure[node] > max_degree:
                max_degree = centrality_measure[node]
                rep = node
        highest_degree_representatives[rep] = max_degree
    # nlargest = heapq.nlargest(seed, [(degree, node) for node, degree in highest_degree_representatives.items()])
    strategy = [node for node in highest_degree_representatives]
    return strategy

def communicability_strategy(G, seed):
    communicability = nx.communicability_exp(G)
    centrality_measure = nx.harmonic_centrality(G)
    highest_degree_node = max(centrality_measure, key=centrality_measure.get)
    max_node_comm = communicability[highest_degree_node]
    nlargest = heapq.nlargest(seed, [(val, node) for node, val in max_node_comm.items()])
    strategy = [node for (_, node) in nlargest]
    return strategy

def mixed_strategy(G, seed):
    deg_cen = degree_centrality(G)
    close_cen = closeness_centrality(G)
    cliques = greedy_modularity_communities(G, n_communities=seed)
    N = len(G.nodes)
    deg_sorted = sorted(deg_cen.items(), key=lambda deg_cen:deg_cen[1])
    close_sorted = sorted(close_cen.items(), key=lambda close_cen:close_cen[1])
    scores = defaultdict(int)
    highest_degree_representatives = {}
    for i in range(N):
        scores[deg_sorted[i][0]] += i 
        scores[close_sorted[i][0]] += i 
    for clique in cliques:
        max_degree, rep = float('-INF'), None
        for node in clique:
            if scores[node] > max_degree:
                max_degree = scores[node]
                rep = node
        highest_degree_representatives[rep] = max_degree
    for node in scores:
        if node in highest_degree_representatives:
            scores[node] += 5
    sorted_scores = sorted(scores.items(), key=lambda scores:scores[1], reverse=True)
    res = [sorted_scores[i][0] for i in range(seed)]
    return res



if __name__=='__main__':
    if RUN_ALL_GRAPHS:
        for file in os.listdir(GRAPH_DIR):
            graph_file = os.path.join(GRAPH_DIR, file)
            if not os.path.isfile(graph_file):
                raise Exception('Not a file!')
            G, seed, adj_list = testing.read_graph(graph_file)
    else:
        G, seed, adj_list = testing.read_graph(GRAPH_DIR+'/'+SINGLE_GRAPH)
        communicability_strategy(G, seed)

        
        






            
