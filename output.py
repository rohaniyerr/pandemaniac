from testing import max_neighbors_strat, centrality_strategy, output_to_submission, read_graph
from testing import output_random_strategy
from other_strategies import communicability_strategy, mixed_strategy3, mixed_strategy2
from spectral_clustering import spectral_strategy
import sim

GRAPH_FILE = 'J.25.33.json'

if __name__ == '__main__':
    G, seed, adj_list = read_graph('graphs/' + GRAPH_FILE)
    output_random_strategy(G, seed, GRAPH_FILE)
    #strat = max_neighbors_strat(G, seed)
    #strat = centrality_strategy(G, seed, 'eigenvector')
    com_strat = communicability_strategy(G, seed)
    spec_strat = spectral_strategy(G, seed)
    mixed_strat = mixed_strategy3(G, seed)
    max_strat = max_neighbors_strat(G, seed)
    base_strat = centrality_strategy(G, seed, 'degree')
    print(com_strat)
    print(spec_strat)
    print(mixed_strat)
    print(max_strat)
    strats = [com_strat, spec_strat, mixed_strat, max_strat]
    diffs = {i:0 for i in range(len(strats))}
    for i in range(len(strats)):
        for j in range(i+1, len(strats)):
            strat_dict = {i:strats[i],j:strats[j]}
            result = sim.run(adj_list, strat_dict)
            if result[i] > result[j]:
                diffs[i] += result[i] - result[j]
                diffs[j] -= result[i] - result[j]
            elif result[j] > result[i]:
                diffs[j] += result[j] - result[i]
                diffs[i] -= result[j] - result[i]
    print(diffs)
    max_diff = 2**-31
    best_strat = None
    for i in diffs:
        if diffs[i] > max_diff:
            max_diff = diffs[i]
            best_strat = i
        if diffs[i] == max_diff:
            resulti = sim.run(adj_list, {i:strats[i], 'base':base_strat})
            resultmax = sim.run(adj_list, {best_strat:strats[best_strat], 'base':base_strat})
            if resulti[i] > resultmax[best_strat]:
                best_strat = i
    strat = strats[best_strat]
    print(strat)
    print(sim.run(adj_list, {best_strat:strat, 'base':base_strat}))
    output_file = 'submissions/' + ''.join(GRAPH_FILE.split('.')[:3]) + '.txt'
    output_to_submission(GRAPH_FILE, strat, '')
