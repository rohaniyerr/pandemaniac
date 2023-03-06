import requests
BASE_URL = 'http://52.9.240.217/'
NUM_SECTIONS = 10
GRAPHS = ['G.10.11', 'G.10.12', 'O.10.13', 'O.10.14']
def extract_data():
    graph_data = {}
    payload = {
        'username': 'rosa',
        'password': 'eYdFLA5AaPDV'
    }
    with requests.Session() as s:
        for graph in GRAPHS:
            _ = s.post(BASE_URL+'login', data=payload)
            resp = s.get(BASE_URL+'submit/'+graph)
            data = resp.text
            section_indices = [data.find(f'id="section-{i}"') for i in range(NUM_SECTIONS)]
            section_data = {}
            for j in range(NUM_SECTIONS):
                if j == NUM_SECTIONS-1:
                    max_deg_idx = data.find('max degree', section_indices[j])
                    num_nodes_idx = data.find('number of nodes', section_indices[j])
                    total_deg_idx = data.find('total degrees', section_indices[j])
                else:
                    max_deg_idx = data.find('max degree', section_indices[j], section_indices[j+1]-1)
                    num_nodes_idx = data.find('number of nodes', section_indices[j], section_indices[j+1]-1)
                    total_deg_idx = data.find('total degrees', section_indices[j], section_indices[j+1]-1)
                max_deg = ''.join(filter(str.isdigit, data[max_deg_idx+1:max_deg_idx+100]))
                num_nodes = ''.join(filter(str.isdigit, data[num_nodes_idx+1:num_nodes_idx+100]))
                total_deg = ''.join(filter(str.isdigit, data[total_deg_idx+1:total_deg_idx+100]))
                section_data[j] = [float(max_deg), float(num_nodes), float(total_deg)]
            graph_data[graph] = section_data 
    return graph_data  

    

        
