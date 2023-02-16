import networkx as nx
import json
import sim
from testing import combine_cluster_centrality, read_graph, max_neighbors_strat, copy_ta_strat2, centrality_strategy
from spectral_clustering import spectral_strategy
from other_strategies import dominating_strategy, clique_strategy, communicability_strategy, mixed_strategy, mixed_strategy2, mixed_strategy3
import matplotlib.pyplot as plt
import os

TEAM_DIR = 'snap_strats/'
GRAPH_DIR = 'graphs/'

def file_to_strat(file, team_name):
    with open(file) as jsonfile:
        strat_list = json.load(jsonfile)
        return strat_list[team_name]

if __name__ == '__main__':
    overall_wins = 0
    overall_draws = 0
    overall_losses = 0
    for file in os.listdir(TEAM_DIR):
        if file == '.DS_Store':
            continue
        tmp = file.split('-')
        team_name, graph_type = tmp[1].split('.')[0], tmp[0]
        graph_filename = GRAPH_DIR+graph_type+'.json'
        G, seed, adj_list = read_graph(graph_filename)
        team_file = os.path.join(TEAM_DIR, file)
        team_strat = file_to_strat(team_file, team_name)
        strat_dict = {}
        wins = 0 
        draws = 0
        rounds = 50
        our_strat = clique_strategy(G, seed)
        strat_dict['strategy'] = our_strat
        for i in range(rounds):
            strat_dict[team_name] = team_strat[i]
            result = sim.run(adj_list, strat_dict)
            if result['strategy'] > result[team_name]:
                wins += 1
            elif result['strategy'] == result[team_name]:
                draws += 1
            # print(result)
        losses = rounds - wins - draws
        print(f'{file}: {wins}-{draws}-{losses}')
        if wins > losses:
            overall_wins += 1
        elif losses > wins:
            overall_losses += 1
        else:
            overall_draws += 1
    print(f'Overall record: {overall_wins}-{overall_draws}-{overall_losses}')
