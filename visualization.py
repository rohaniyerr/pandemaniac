import pandemaniac as pan
import networkx as nx

def open_saved_network(filename):
    saved_network = nx.read_gpickle(filename)
    return saved_network

if __name__=='__main__':
    web = 'caltech.gpickle'
    G = open_saved_network(web)
    nodes = list(G.nodes())
    nodes_to_idx = {}
    for i in range(len(nodes)):
        nodes_to_idx[nodes[i]] = i
    adj_list = {}
    for i in range(len(nodes)):
        adj_list[i] = []
        for j in nx.neighbors(G, nodes[i]):
            adj_list[i].append(nodes_to_idx[j])
    seed = {"strategy1": [0, 1, 2]}
    pan.viz(adj_list, seed)