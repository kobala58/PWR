import networkx as nx
import pandas as pd
from pyvis.network import Network
import numpy as np

def open_data(filename: str="./data.csv", named_row: bool = False) -> pd.DataFrame:
    if named_row:
        data = pd.read_csv(filename, index_col=0)
    else: 
        data = pd.read_csv(filename)

    return data

def create_matrix(names: list, data: pd.DataFrame):
    print(len(names))
    names = list(names[0:50])
    names.remove("Poza stacją")
    table = [[0 for x in range(len(names))] for _ in range(len(names))]

    for x,valx in enumerate(names):
        for y,valy in enumerate(names):
            print(f"{x}/{y} of {len(names)}")
            table[x][y] = len(data[
                (data["rental_place"] == valx) &
                (data["return_place"] == valy)
                ])

    for row in table:
        print(row)

    df = pd.DataFrame(table, columns=names, index=names)
    df.to_csv("./matrix.csv")
    return df

def create_graph(matrix: pd.DataFrame):
    val = matrix.values.tolist()
    net = Network(directed=True)
    ret_nx_net = nx.Graph()
    names = list(matrix.columns.values)
    
    for x in names:
        net.add_node(x, label=x)
        ret_nx_net.add_node(x, label=x)

    for x,valx in enumerate(val):
        for y,valy in enumerate(val):
            if (type(val[x][y]) != int):
                # print(f"{names[x]} !+! {val[x][y]} !+! {names[y]}")
                continue
            elif (val[x][y] < MINIMAL_CONN_CNT):
                continue
            else:
                ret_nx_net.add_edge(names[x], names[y], weight=val[x][y])
                net.add_edge(names[x], names[y], weight=val[x][y])
    
    

    net.toggle_physics(False)
    net.show_buttons(filter_=["physics"])
    net.save_graph('mygraph.html')
    
    return ret_nx_net

def generate_graph_info(data: nx.Graph, output: str):
    # print(list(nx.isolates(data))) 
    data.remove_nodes_from(list(nx.isolates(data)))
    data.remove_nodes_from(['Unnamed: 0'])
    # print(nx.is_connected(data))


    betweenness = nx.betweenness_centrality(data, normalized=True, endpoints=False)
    edge_betweenness = nx.edge_betweenness_centrality(data, normalized=True)

    #get random node
    nd = np.random.choice(data.nodes())
    # Pośrednictwo

    print(f"Węzeł z maksymalnym pośrednictwem: {max(betweenness, key=betweenness.get)} - {max(betweenness.values())} ")

    # K-spójność

    print(f"K-spójność wierzchołkowa: {nx.node_connectivity(data)} ")
    print(f"K-spójność krawędziowa: {nx.edge_connectivity(data)} ")

    # Kliki

    print(f"Największa klika w grafie oraz ich liczba: {max([len(x) for x in list(nx.find_cliques(data))])}, {len(list(nx.find_cliques(data)))}")

    # Pośrednictwo krawędzi

    print(f"Krawędź z maksymalnym pośrednictwem: {max(edge_betweenness, key=edge_betweenness.get)} - {max(edge_betweenness.values())} ")
    print(f"Krawędź z minimalnym pośrednictwem: {min(edge_betweenness, key=edge_betweenness.get)} - {min(edge_betweenness.values())} ")

    info = {
            "is_conected": nx.is_connected(data),
            "degree": len(data),
            "size": len(data.edges()),
            "density": nx.density(data),
            "diameter": nx.diameter(data),
            "avg_path_len": nx.average_shortest_path_length(data),
            "rnd_node_name": nd,
            "rnd_node_defree": nx.degree(data, nd),
            "avg_closeness_centr": nx.closeness_centrality(data, u=nd),
            }
    
    for key, val in info.items():
        print(f"{key}: {val}")
    # print(info)

MINIMAL_CONN_CNT = 50


if __name__ == "__main__":
    # data = open_data()
    # all_places = data["rental_place"].unique()
    # matrix = create_matrix(names=all_places, data=data)
    data = open_data("./matrix.csv")
    nx_data = create_graph(matrix=data)
    generate_graph_info(data=nx_data, output="output_info.json")
    # print(data)
