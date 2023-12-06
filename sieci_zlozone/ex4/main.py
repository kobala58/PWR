import networkx as nx
import numpy as np
import pandas as pd
from networkx.algorithms.bipartite import spectral
from pyvis.network import Network
import matplotlib.pyplot as plt
from networkx.algorithms import community
from networkx.algorithms.community import greedy_modularity_communities

# from networkx.algorithms.cluster import
from scipy.cluster import hierarchy

def open_data(filename: str = "./data.csv", named_row: bool = False) -> pd.DataFrame:
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

    for x, valx in enumerate(names):
        for y, valy in enumerate(names):
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

    for x, valx in enumerate(val):
        for y, valy in enumerate(val):
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
    # print(nx.is_connected(data))

    # vtx = np.random.choice(graph.nodes())

    info = {
        "degree": len(data),
        "size": len(data.edges()),
        "density": nx.density(data),
        "diameter": nx.diameter(data),
        "avg_path_len": nx.average_shortest_path_length(data)
    }
    print(info)


MINIMAL_CONN_CNT = 50


def task3(G: nx.Graph):
    cliques = list(nx.find_cliques(G))
    print("Kliki:", cliques)

    modularity_communities = list(greedy_modularity_communities(G))
    print("Moduły:")
    for x in modularity_communities:
        print(x)

    distance_matrix = nx.to_numpy_array(G)
    Z = hierarchy.linkage(distance_matrix, method='complete')
    plt.figure(figsize=(10, 5))
    dn = hierarchy.dendrogram(Z)
    plt.title('Dendrogram')
    plt.show()

    # 3. Metody podziałowe
    # Girvan-Newman algorithm
    gn_communities = list(community.girvan_newman(G))
    print("Metoda podziałowa - Girvan-Newman:", list(sorted(c) for c in gn_communities))

    # 4. Porównanie metody aglomeracyjnej i metod podziałowych za pomocą modularności
    modularity_agglomerative = community.modularity(G, modularity_communities)
    print("Modularność - Metoda aglomeracyjna:", modularity_agglomerative)

    # 5. Podział sieci na dwa rozłączne zbiory węzłów za pomocą metody podziału spektralnego
    laplacian_matrix = nx.laplacian_matrix(G).toarray()
    eigenvalues, eigenvectors = np.linalg.eig(laplacian_matrix)
    fiedler_vector = eigenvectors[:, 1]  # Drugi wektor własny

    # Podział wierzchołków na dwie części na podstawie wartości wektora Fiedlera
    subset1 = [node for node, value in enumerate(fiedler_vector) if value >= 0]
    subset2 = [node for node, value in enumerate(fiedler_vector) if value < 0]

    print("Podział spektralny - Zbiór 1:", subset1)
    print("Podział spektralny - Zbiór 2:", subset2)

    # 6. Badanie hierarchicznej struktury sieci
    distance_matrix = nx.to_numpy_array(G)
    Z = hierarchy.linkage(distance_matrix, method='complete')
    plt.figure(figsize=(10, 5))
    dn = hierarchy.dendrogram(Z)
    plt.title('Dendrogram')
    plt.show()



if __name__ == "__main__":
    data = open_data("./matrix.csv")
    nx_data = create_graph(matrix=data)
    #generate_graph_info(data=nx_data, output="output_info.json")
    task3(nx_data)
