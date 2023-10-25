import networkx as nx
import pandas as pd
from pyvis.network import Network

def open_data(filename: str="./data.csv", named_row: bool = False) -> pd.DataFrame:
    if named_row:
        data = pd.read_csv(filename, index_col=0)
    else: 
        data = pd.read_csv(filename)

    return data

def create_matrix(names: list, data: pd.DataFrame):
    print(len(names))
    names = names[0:60]
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

    names = list(matrix.columns.values)
    
    for x in names:
        net.add_node(x, label=x)

    for x,valx in enumerate(val):
        for y,valy in enumerate(val):
            if (type(val[x][y]) != int):
                print(f"{names[x]} !+! {val[x][y]} !+! {names[y]}")
                continue
            elif (val[x][y] < 5):
                continue
            else:
                net.add_edge(names[x], names[y], weight=val[x][y])
    
    net.toggle_physics(False)
    net.show_buttons(filter_=["physics"])
    net.save_graph('mygraph.html')




if __name__ == "__main__":
    # data = open_data()
    # all_places = data["rental_place"].unique()
    # matrix = create_matrix(names=all_places, data=data)
    data = open_data("./matrix.csv")
    create_graph(matrix=data)
    # print(data)
