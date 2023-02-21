import networkx as nx
import json
import sim
from testing import combine_cluster_centrality, read_graph, max_neighbors_strat, max_neighbors_strat2, centrality_strategy
from spectral_clustering import spectral_strategy
from other_strategies import dominating_strategy, clique_strategy, communicability_strategy, mixed_strategy, mixed_strategy2, mixed_strategy3
import matplotlib.pyplot as plt
import os
from networkx import clustering, triangles
from networkx import degree_centrality, closeness_centrality, betweenness_centrality, eigenvector_centrality

BASE_DIR = 'base_strats/'
GRAPH_DIR = 'graphs/'

def file_to_strat(file, team_name):
    with open(file) as jsonfile:
        strat_list = json.load(jsonfile)
        return strat_list[team_name]

if __name__ == '__main__':
    for file in os.listdir(BASE_DIR):
        tmp = file.split('-')
        team_name, graph_type = tmp[1].split('.')[0], tmp[0]
        graph_filename = GRAPH_DIR+graph_type+'.json'
        print(graph_filename)
        G, seed, adj_list = read_graph(graph_filename)
        base_file = os.path.join(BASE_DIR, file)
        base_strat = file_to_strat(base_file, team_name)
        print(base_strat[0])
        deg_cen = degree_centrality(G)
        close_cen = closeness_centrality(G)
        bet_cen = betweenness_centrality(G)
        eig_cen = eigenvector_centrality(G)
        clust = clustering(G)
        tris = triangles(G)

        sorted_deg = sorted(deg_cen.items(), key=lambda deg_cen:deg_cen[1], reverse=True)
        sorted_close = sorted(close_cen.items(), key=lambda close_cen:close_cen[1], reverse=True)
        sorted_bet = sorted(bet_cen.items(), key=lambda bet_cen:bet_cen[1], reverse=True)
        sorted_eig =  sorted(eig_cen.items(), key=lambda eig_cen:eig_cen[1], reverse=True)
        sorted_clust = sorted(clust.items(), key=lambda clust:clust[1], reverse=True)
        sorted_tris = sorted(tris.items(), key=lambda tris:tris[1], reverse=True)

        print([x[0] for x in sorted_deg[:15]])
        print([x[0] for x in sorted_close[:15]])
        print([x[0] for x in sorted_bet[:15]])
        print([x[0] for x in sorted_eig[:15]])
        print([x[0] for x in sorted_clust[:15]])
        print([x[0] for x in sorted_tris[:15]])

        max_strat = max_neighbors_strat(G, seed)
        mixed_strat2 = mixed_strategy2(G, seed)
        mixed_strat3 = mixed_strategy3(G, seed)
        com_strat = communicability_strategy(G, seed)
        strats = {'max':max_strat, 'mixed2':mixed_strat2, 'mixed3':mixed_strat3, 'com':com_strat}
        strat_dict = {'ta_base':base_strat[0]}
        for strat in strats:
            print(strats[strat])
            strat_dict = {'ta_base':base_strat[0], strat:strats[strat]}
            result = sim.run(adj_list, strat_dict)
            print(result)
        #print(sim.run(adj_list, {'max':max_strat, 'mixed':mixed_strat}))
        print('\n')
