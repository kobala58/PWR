import networkx as nx
import json
import matplotlib.pyplot as plt
from pyvis.network import Network
import random



def create_graph(filename: str):
    with open(f"./{filename}", "r") as file:
        data = json.load(file) #importing data
    parsed_data = []
    print(len(set([x["name"] for x in data])))
    for y in range(0,len(data)):
        for x in range(0, len(data)):
            if x == y:
                continue
            if y > x:
                continue
            conn = len(set(data[x]["contributors"]) & set(data[y]["contributors"]))
            if conn != 0:
                tmp = (data[x]["name"], data[y]["name"], conn)
                parsed_data.append(tmp)

    G = nx.Graph()
    G.add_nodes_from([(x["name"], {"size": x["number"]}) for x in data])

    print(len(list(G.nodes)))
    G.add_weighted_edges_from(parsed_data)
    nx.write_gexf(G, "test.gexf")
    return G,[x["name"] for x in data]
    

def check_distance(G: nx.Graph, a:str, b:str):
    print(f'Distance between {a} and {b}:')
    try: 
        val = nx.shortest_path(G, source=a, target=b)
    except nx.NetworkXNoPath:
        return -1
    print(val)
    return val

if __name__ == "__main__":
    graph,nodes_name = create_graph("results.json")
    check_distance(graph, random.choice(nodes_name), random.choice(nodes_name))
    print(f"Is eulerian: {nx.is_eulerian(graph)}")

    
