from dataclasses import dataclass, field
import json
from sys import path
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
# import seaborn.apionly as sns
import matplotlib.animation
import math

@dataclass
class Graph:
    filename: str
    graph: dict = field(init=False)
    parsed_graph: dict = field(init=False)
    dfs_hist: list = field(init=False)
    curr_graph: nx.Graph = field(init=False)
    G: nx.Graph = field(init=False)
    
    def __post_init__(self):
        with open(self.filename + ".json", "r") as file:
            self.graph = json.load(file)
        tmp = []
        self.G = nx.Graph()
        self.nodes = self.graph["vertexes"]
        self.cnt = len(self.nodes)
        for key,val in self.graph["pairs"].items():
            for n,w in val:
                tmp.append((key, n, int(w)))
        self.G.add_weighted_edges_from(tmp) # insert edges
        
    def draw(self, colored=None):
        # self.G = nx.from_dict_of_lists(self.parsed_graph)
        # print(self.G)
        # pos = nx.spring_layout(self.G)
        # nx.draw(self.G)
        # plt.show()
        pos=nx.spring_layout(self.G) # pos = nx.nx_agraph.graphviz_layout(G)
        if colored:
            colors = []
            for x in self.G.nodes:
                if x in colored:
                    colors.append("green")
                else:
                    colors.append("blue")

            nx.draw_networkx(self.G,pos, with_labels=True, node_color=colors)
        else:
            nx.draw_networkx(self.G,pos, with_labels=True)
        labels = nx.get_edge_attributes(self.G,'weight')
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=labels)
        plt.show()
    
    def draw_curr(self, visited):
        self.curr_graph = nx.Graph()
        for x in visited:
            tmp = self.parsed_graph[x]
            self.curr_graph.add_node(x)
            for letter in tmp:
                if letter not in visited:
                    continue
                else:
                    self.curr_graph.add_node(letter)
                    self.curr_graph.add_edge(x, letter)
        nx.draw(self.curr_graph, with_labels = True)
        plt.show()

    def draw_graph(self, g: nx.Graph):
        import matplotlib.pyplot as plt
        pos=nx.spring_layout(g) # pos = nx.nx_agraph.graphviz_layout(G)
        nx.draw_networkx(g,pos, with_labels=True)
        labels = nx.get_edge_attributes(g,'weight')
        nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)

        plt.show()

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start)  # Możesz dostosować to zależnie od Twojego przypadku użycia
        self.draw_curr(visited)
        for neighbor in self.parsed_graph[start]:
            if neighbor not in visited:
                self.dfs(neighbor, visited)
    
    def kruskal(self):
        edges = []
        for u,v,a in self.G.edges(data=True):
            edges.append((a["weight"], v, u))
        edges.sort()
        print(edges)
        num_vertices = len(self.G.nodes)
        print(num_vertices)
        mst = []
        union_find = UnionFind(num_vertices)

        for weight, u, v in edges:
            print(weight, u, v)
            if union_find.find(u) != union_find.find(v):
                union_find.union(u, v)
                mst.append((u, v, weight))

        return mst
    
    def convert_to_matrix(self):
        edg = list(self.G.edges(data=True))
        print("test")
        nd = list(self.G.nodes())
        self.am = [[0 for _ in nd] for __ in nd]
        for x in range(len(nd)): 
            print(nd[x], self.G.edges(nd[x], data="weight"))
            for y in range(len(nd)):
                res = self.G.get_edge_data(nd[x], nd[y], default=0)
                if type(res) == int:
                    self.am[x][y] = res
                else:
                    self.am[x][y] = res["weight"]

    def msp(self):
        # Prim's Algorithm in Python
        self.convert_to_matrix()
        names = list(self.G.nodes)
        N = len(self.G.nodes)
        selected_node = [0 for _ in self.G.nodes]

        no_edge = 0

        selected_node[0] = True
        steps = []
        # printing for edge and weigh
        print("Edge : Weight\n")
        while (no_edge < N - 1):
            minimum = math.inf
            a = 0
            b = 0
            for m in range(N):
                if selected_node[m]:
                    for n in range(N):
                        if ((not selected_node[n]) and self.am[m][n]):  
                            # not in selected and there is an edge
                            if minimum > self.am[m][n]:
                                minimum = self.am[m][n]
                                a = m
                                b = n
            steps.append((names[a], names[b], self.am[a][b]))
            print(names[a] + "-" + names[b] + ":" + str(self.am[a][b]))
            tmp = nx.Graph()
            tmp.add_weighted_edges_from(steps)
            self.draw_graph(tmp)
            selected_node[b] = True
            no_edge += 1
    
    def dijkstra_algorithm(self, start_node, end_node):
        unvisited_nodes = list(self.G.nodes)
     
        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
        shortest_path = {}
     
        # We'll use this dict to save the shortest known path to a node found so far
        previous_nodes = {}
 
        # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
        max_value = math.inf

        for node in unvisited_nodes:
            shortest_path[node] = max_value
        # However, we initialize the starting node's value with 0   
        shortest_path[start_node] = 0
        
        # The algorithm executes until we visit all nodes
        while unvisited_nodes:
            # The code block below finds the node with the lowest score
            current_min_node = None
            for node in unvisited_nodes: # Iterate over the nodes
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node
                    
            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = self.G.edges(current_min_node, data="weight")

            for neighbor_ in neighbors:
                neighbor = neighbor_[1]
                # tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
                tentative_value = shortest_path[current_min_node] + self.G.get_edge_data(current_min_node, neighbor)["weight"]
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node
     
            # After visiting its neighbors, we mark the node as "visited"
            unvisited_nodes.remove(current_min_node)

        path = []
        node = end_node
        while node != start_node:
            path.append(node)
            node = previous_nodes[node]

        path.append(start_node)
        print(" -> ".join(reversed(path)))
        self.draw(colored=path)

    def searching_algo_BFS(self, s, t, parent):

        visited = [False for _ in self.nodes]
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.ff[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False


    def ford_fulkerson(self, source, sink):
        self.convert_to_matrix()
        self.ff = self.am
        source = self.nodes.index(source)
        sink = self.nodes.index(sink)
        parent = [-1 for _ in self.nodes]
        max_flow = 0

        while self.searching_algo_BFS(source, sink, parent):

            path_flow = math.inf
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.ff[parent[s]][s])
                s = parent[s]

            # Adding the path flows
            max_flow += path_flow

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                self.ff[u][v] -= path_flow
                self.ff[v][u] += path_flow
                v = parent[v]

        return max_flow

if __name__ == "__main__":
    test = Graph("test_graph")
    print(test.G)
    # test.dijkstra_algorithm("A", "H")
    print(test.ford_fulkerson("D", "A"))
