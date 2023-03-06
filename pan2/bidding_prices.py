import htmlparser
import heapq
def best_node_score(max_deg, num_nodes, total_deg):
    score = 1e5*(max_deg/total_deg)/num_nodes
    return score

def average_node_score(max_deg, num_nodes, total_deg):
    score = (total_deg - max_deg) / (num_nodes - 1)
    return score

if __name__=='__main__':
    graph_data = htmlparser.extract_data()
    graph_scores = {}
    for graph in graph_data:
        section_scores = {}
        section_data = graph_data[graph]
        for section in section_data :
            max_degree,num_nodes,total_degree = section_data[section]
            prob_good_nodes = best_node_score(max_degree,num_nodes,total_degree)
            prob_avg_node = average_node_score(max_degree,num_nodes,total_degree)
            section_scores[section] = prob_good_nodes+prob_avg_node
        graph_scores[graph] = section_scores
    for graph in graph_scores:
        print(graph, sorted(graph_scores[graph].items(), key=lambda x:x[1]),'\n\n\n')

