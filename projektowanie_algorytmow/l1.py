from enum import Flag
from math import sin, sqrt, cos
import math
from typing import List
import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib
matplotlib.use('tkagg')


def generate_nodes_from_input() -> tuple[nx.Graph, int]:
    nodes_count = int(input("Podaj ilosc wierzcholkow: "))
    G = nx.Graph()
    G.add_nodes_from(range(nodes_count))
    return (G, nodes_count)

def ex_1():
    RADIUS = 10
    G, nodes_count = generate_nodes_from_input()
    G.add_edges_from([(x,y) for x in range(nodes_count) for y in range(nodes_count) if x != y])
    G.remove_edge(1, 3)
    # pos = nx.circular_layout(G) simple solution provided by Networkx libary
    # we need to implement own solution based on polar coordinate system
    __space = 360/nodes_count # separtaor 
    # pos = {x:[(RADIUS*cos(__space*x)).__round__(2), (RADIUS*sin(__space*x)).__round__(2)] for x in range(nodes_count)}
    pos = {}
    for x in range(nodes_count):
        print(__space * x)
        angle = (__space * x)*math.pi/180 
        pos[x] = [(RADIUS*cos(angle)).__round__(2), (RADIUS*sin(angle)).__round__(2)] 

    fig, ax = plt.subplots() #create canvas
    print(pos)
    nx.draw(G, pos=pos)
    nx.draw_networkx_labels(G, pos)
    plt.axis("on")
    ax.add_patch(plt.Circle((0,0), RADIUS, fill=False, color="green"))
    ax.set_xlim(-12,12)
    ax.set_ylim(-12,12) # temp solution 
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()

def ex_2():
    RANGSIZE_DOWN = 0
    RANGSIZE_UP = 100
    G, nodes_count = generate_nodes_from_input() # grab graph from user input
    fig, ax = plt.subplots() #create canvas
    pos = {x:[random.randint(RANGSIZE_DOWN,RANGSIZE_UP), random.randint(RANGSIZE_DOWN,RANGSIZE_UP)] for x in range(nodes_count)} # position in dictionary
    nx.draw(G, pos=pos, ax=ax)
    nx.draw_networkx_labels(G, pos=pos)
    plt.axis("on")
    ax.set_xlim(RANGSIZE_DOWN-0.1*RANGSIZE_DOWN, RANGSIZE_UP+0.1*RANGSIZE_UP)
    ax.set_ylim(RANGSIZE_DOWN-0.1*RANGSIZE_DOWN, RANGSIZE_UP+0.1*RANGSIZE_UP)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()

def ex_3():
    RANGSIZE_DOWN = 0
    RANGSIZE_UP = 100
    RADIUS = 5
    G, nodes_count = generate_nodes_from_input()
    G = nx.Graph() # non optimal solution but i dont want to repeat code

    fig, ax = plt.subplots() #create canvas
    cnt = 0
    points = [] #[node number, x, y]
    pos = dict()
    for node in range(nodes_count):
        iter = 0
        while iter<100:
            flag = True
            x = random.randint(RANGSIZE_DOWN,RANGSIZE_UP)
            y = random.randint(RANGSIZE_DOWN,RANGSIZE_UP)
            for point in points:
                dist = sqrt((x-point[1])**2+(y-point[2])**2)
                if dist < RADIUS*2:
                    flag = False
                    break
            if flag:
                points.append([node,x,y])
                pos[node] = [x,y]
                ax.add_patch(plt.Circle((x,y), RADIUS, fill=False))
                G.add_node(node)
                break
            else:
                iter+=1            
        if iter == 100:
            print(f"Cannot find space to allocate node number {node}")
            print("Showing result")
        else:
            print("All circles allocated")
            print("Showing result")
    
    nx.draw(G, pos=pos, ax=ax)
    nx.draw_networkx_labels(G, pos=pos)
    plt.axis("on")
    ax.set_xlim(RANGSIZE_DOWN-0.1*RANGSIZE_DOWN, RANGSIZE_UP+0.1*RANGSIZE_UP)
    ax.set_ylim(RANGSIZE_DOWN-0.1*RANGSIZE_DOWN, RANGSIZE_UP+0.1*RANGSIZE_UP)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()

if __name__ == "__main__":
    ex_1()
    ex_2()
    ex_3()
