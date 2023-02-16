import networkx as nx
from networkx import square_clustering, clustering, triangles
from networkx import degree_centrality, closeness_centrality, betweenness_centrality, eigenvector_centrality, pagerank
import json
import random
import sim
import matplotlib.pyplot as plt
import heapq
from sklearn.cluster import KMeans, SpectralClustering
import os
import testing
from sklearn import cluster
from sklearn import manifold
from collections import defaultdict
import numpy as np
GRAPH_DIR = 'graphs'
RUN_ALL_GRAPHS = False
SINGLE_GRAPH = 'J.5.10.json'

def kmeans(X, k):
    kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto").fit(X)
    return kmeans.labels_, kmeans.cluster_centers_

def spectral_clustering(X, k):
    spec = SpectralClustering(n_clusters=k, random_state=0, 
                              assign_labels='discretize',
                              affinity='nearest_neighbors').fit(X)
    return spec.labels_

def spectral_strategy(G, seed):
    A = nx.adjacency_matrix(G)
    labels = spectral_clustering(A, 2)
    clust_0 = {node:labels[i] for i, node in enumerate(list(G.nodes)) if labels[i]== 0}
    clust_1 = {node:labels[i] for i, node in enumerate(list(G.nodes)) if labels[i]== 1}
    degrees = pagerank(G)
    degree_clust_0 = {node:degrees[str(node)] for node in clust_0}
    degree_clust_1 = {node:degrees[str(node)] for node in clust_1}
    highest_node_0 = max(degree_clust_0, key = degree_clust_0.get)
    highest_node_1 = max(degree_clust_1, key = degree_clust_1.get)
    node_0_neighbors = nx.neighbors(G,highest_node_0)
    node_1_neighbors = nx.neighbors(G,highest_node_1)
    strategy = [highest_node_0, highest_node_1]
    neighbor_degrees_0 = [(degree_clust_0[node], node) for node in node_0_neighbors if node in clust_0]
    neighbor_degrees_1 = [(degree_clust_1[node], node) for node in node_1_neighbors if node in clust_1]
    nlargest_0 = heapq.nlargest(seed//2-1, neighbor_degrees_0)
    nlargest_1 = heapq.nlargest(seed//2-1, neighbor_degrees_1)
    strategy.extend([node for (_,node) in nlargest_0]+[node for (_,node) in nlargest_1])
    return strategy

def plot_clustering(G, k):
    A = nx.adjacency_matrix(G)
    Klabels, centers = kmeans(A, k)
    # print(centers)
    SC_labels = spectral_clustering(A, k)
    plt.figure()
    plt.title('KMeans')
    nx.draw_networkx(G, node_color=Klabels, with_labels=True)
    plt.figure()
    plt.title('Spectral Clustering')
    nx.draw_networkx(G, node_color=SC_labels, with_labels=True)
    plt.show()

if __name__=='__main__':
    if RUN_ALL_GRAPHS:
        for file in os.listdir(GRAPH_DIR):
            graph_file = os.path.join(GRAPH_DIR, file)
            if not os.path.isfile(graph_file):
                raise Exception('Not a file!')
            G, seed, adj_list = testing.read_graph(graph_file)
    else:
        G, seed, adj_list = testing.read_graph(GRAPH_DIR+'/'+SINGLE_GRAPH)
        spectral_ord = nx.spectral_ordering(G)
