from testing import max_neighbors_strat, centrality_strategy, output_to_submission, read_graph
from testing import output_random_strategy
from other_strategies import communicability_strategy
from spectral_clustering import spectral_strategy

GRAPH_FILE = 'RR.10.52.json'

if __name__ == '__main__':
    G, seed, _ = read_graph('graphs/' + GRAPH_FILE)
    #output_random_strategy(G, seed, GRAPH_FILE)
    #strat = max_neighbors_strat(G, seed)
    #strat = centrality_strategy(G, seed, 'eigenvector')
    com_strat = communicability_strategy(G, seed)
    spec_strat = spectral_strategy(G, seed)
    output_file = 'submissions/' + ''.join(GRAPH_FILE.split('.')[:3]) + 'comspec' + '.txt'
    strategy_string = ''
    for _ in range(30):
        for node in spec_strat:
            strategy_string += node + '\n'
    for _ in range(20):
        for node in com_strat:
            strategy_string += node + '\n'
    f = open(output_file, 'w')
    f.write(strategy_string)
    f.close()
    #output_to_submission(GRAPH_FILE, com_strat, 'com')
