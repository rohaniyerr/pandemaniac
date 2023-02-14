import networkx as nx
import json
import sim
from testing import combine_cluster_centrality, read_graph

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
        strat_dict['strategy'] = combine_cluster_centrality(G, seed, c_type='closeness')
        strat_dict[level] = ta_strats[level]
        result = sim.run(adj_list, strat_dict)
        print(result)
