import networkx as nx
import matplotlib.pyplot as plt
from sim_teams import file_to_strat
import os
from testing import read_graph
from other_strategies import mixed_strategy


TEAM_DIR = 'team_strats/'
GRAPH_DIR = 'graphs/'

def open_saved_network(filename):
    saved_network = nx.read_gpickle(filename)
    return saved_network

def draw_graph(G, our_strategy, team_strategy):
    pos = nx.spring_layout(G)
    set_strat_team, set_strat_our = set(team_strategy),set(our_strategy)
    overlapping_nodes = set_strat_team.intersection(set_strat_our)
    team_different_nodes = set_strat_team.difference(overlapping_nodes)
    our_different_nodes = set_strat_our.difference(overlapping_nodes)
    uncolored_nodes = set(G.nodes()) - set_strat_our - set_strat_team
    nx.draw_networkx_nodes(G, pos, nodelist=list(uncolored_nodes), node_color='#808080')
    nx.draw_networkx_nodes(G, pos, nodelist=list(team_different_nodes), node_color='b')
    nx.draw_networkx_nodes(G, pos, nodelist=list(our_different_nodes), node_color='r')
    nx.draw_networkx_nodes(G, pos, nodelist=list(overlapping_nodes), node_color='g')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.show()
if __name__=='__main__':
    count = 0
    for file in os.listdir(TEAM_DIR):
        count+= 1
        tmp = file.split('-')
        team_name, graph_type = tmp[1].split('.')[0], tmp[0]
        graph_filename = GRAPH_DIR+graph_type+'.json'
        G, seed, adj_list = read_graph(graph_filename)
        team_file = os.path.join(TEAM_DIR, file)
        team_strat = file_to_strat(team_file, team_name)[0]
        our_strat = mixed_strategy(G,seed)
        draw_graph(G, our_strat, team_strat)
        if count==1:
            break