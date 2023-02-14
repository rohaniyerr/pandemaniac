from testing import max_neighbors_strat, centrality_strategy, output_to_submission, read_graph

GRAPH_FILE = 'J.20.21.json'

if __name__ == '__main__':
    G, seed, _ = read_graph('graphs/' + GRAPH_FILE)
    #strat = max_neighbors_strat(G, seed)
    strat = centrality_strategy(G, seed, 'eigenvector')
    output_to_submission(GRAPH_FILE, strat, seed, 'eigenvector')
