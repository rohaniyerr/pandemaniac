import networkx as nx
import json
import sim
from testing import combine_cluster_centrality, read_graph, max_neighbors_strat, copy_ta_strat2
import matplotlib.pyplot as plt

TA_BASE_FILE = 'ta_strats/RR.10.50-TA_baseline.json'
TA_TARGET_FILE = 'ta_strats/RR.10.50-TA_target.json'
TA_HARD_FILE = 'ta_strats/RR.10.50-TA_hard.json'
GRAPH_FILE = 'graphs/RR.10.50.json'

def ta_file_to_strat(ta_file, level):
    with open(ta_file) as jsonfile:
        strat_list = json.load(jsonfile)
        return strat_list[f'TA_{level}'][0]

if __name__ == '__main__':
    G, seed, adj_list = read_graph(GRAPH_FILE)
    ta_base = ta_file_to_strat(TA_BASE_FILE, 'baseline')
    ta_target = ta_file_to_strat(TA_TARGET_FILE, 'target')
    ta_hard = ta_file_to_strat(TA_HARD_FILE, 'hard')
    ta_strats = {'base': ta_base, 'target': ta_target, 'hard': ta_hard}
    for level in ta_strats:
        strat_dict = {}
        strat_dict[level] = ta_strats[level]
        wins = 0 
        draws = 0
        rounds = 1
        for _ in range(rounds):
            #strat_dict['strategy'] = combine_cluster_centrality(G, seed, c_type='betweeness')
            #strat_dict['strategy'] = copy_ta_strat2(G, seed)
            result = sim.run(adj_list, strat_dict)
            if result['strategy'] > result[level]:
                wins += 1
            elif result['strategy'] == result[level]:
                draws += 1
            print(result)
        losses = rounds - wins - draws
        print(f'{level}: {wins}-{draws}-{losses}')
    #plt.figure()
    #nx.draw(G)
    #plt.show()
