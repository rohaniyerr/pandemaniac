import htmlparser

C = 1e5

def best_node_score(max_deg, num_nodes, total_deg):
    score = C*(max_deg/total_deg)/num_nodes
    return score

def average_node_score(max_deg, num_nodes, total_deg):
    score = (total_deg - max_deg) / (num_nodes - 1)
    return score

def connectivity_score(x, n, y): #x = max_degree, n = num_nodes, y = total_degree
    score = 1-((x / (n-1)) * (1 - (1 - y / (n * (n-1)))**n))
    return score

def opportunistic_score(num_nodes, total_degree):
    return total_degree / num_nodes

# greedy score = max_degree

if __name__== '__main__':
    graph_data = htmlparser.extract_data()
    graph_scores = {}
    for graph in graph_data:
        section_scores = {}
        section_data = graph_data[graph]
        for section in section_data:
            max_degree,num_nodes,total_degree = section_data[section]
            total_degree = float(str(total_degree)[1:])
            #best = best_node_score(max_degree,num_nodes,total_degree)
            #avg = average_node_score(max_degree,num_nodes,total_degree)
            opp = opportunistic_score(num_nodes, total_degree)
            conn = connectivity_score(max_degree, num_nodes, total_degree)
            section_scores[section] = opp
        graph_scores[graph] = section_scores
    budget = 160
    # our budget = 603, TA budget = 169
    save = 5
    start = 0
    bid_sections = 10
    for graph in graph_scores:
        best = sorted(graph_scores[graph].items(), key=lambda x:x[1], reverse=True)
        add = min(0,best[-1][1])
        best = [x[1]+abs(add) for x in best]
        c = sum(best[start:start+bid_sections])
        bids = [(budget-save)*(best[i]/c) for i in range(start,start+bid_sections)]
        print(bids)
        print(graph, sorted(graph_scores[graph].items(), key=lambda x:x[1], reverse=True),'\n\n\n')
