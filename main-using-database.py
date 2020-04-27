import requests
import pprint
import env
import json
import pickle
import math

import flexpolyline as fp
from gmplot import gmplot

START_LAT = 17.5449
START_LNG = 78.5718
DEST_LAT = 17.2403
DEST_LNG = 78.4294
VIA_LAT = 17.4033
VIA_LNG = 78.4707
INFINITY = 10000000

with open("distance_matrix_db", "rb+") as file:
    distance_matrix = pickle.load(file)

with open("graph_db", "rb+") as file:
    graph = pickle.load(file)

with open("gmap_db", "rb+") as file:
    gmap = pickle.load(file)


def h_dist_dest(a):

    if distance_matrix.get(a) != None:
        return distance_matrix[a]
    return INFINITY

def distance(a, b):
    p1, p2 = a
    p3, p4 = b
    return math.sqrt(((p3 - p1) ** 2) + ((p4 - p2) ** 2))

# a star implementation

open_list = []
closed_list = []
g = {}
g[(START_LAT, START_LNG)] = 0
parent = {}

open_list.append((0, (START_LAT, START_LNG)))

while len(open_list) > 0:

    node = min(open_list)
    print(node)
    open_list.remove(node)
    closed_list.append(node)

    node = node[1]
    gmap.marker(node[0], node[1], 'brown')

    if (node == (DEST_LAT, DEST_LNG)):
        print("found")
        break

    

    for child in graph[node]:
        print("parent: {}, child: {}".format(node, child))
        g_temp = g[node] + distance(node, child)


        gv = INFINITY
        if g.get(child) != None:
            gv = g[child]

        if gv > g_temp:
            parent[child] = node
            g[child] = g_temp
            # f = g[child] + h_dist_dest(child)
            f = g[child] + distance(child, (DEST_LAT, DEST_LNG))
            if child not in closed_list:
                open_list.append((f, child))
            

pprint.pprint(parent)

path = []

temp_node = (DEST_LAT, DEST_LNG)

while temp_node != (START_LAT, START_LNG):
    path.append(temp_node)
    temp_node = parent[temp_node]

lat_list2, lng_list2 = zip(*path)
gmap.plot(lat_list2, lng_list2, 'darkgreen', edge_width=10)
gmap.draw("my_map.html")