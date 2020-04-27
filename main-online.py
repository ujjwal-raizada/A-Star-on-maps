import requests
import pprint
import env
import json
import math

import flexpolyline as fp
from gmplot import gmplot


API_KEY = '4A-Ns4qs8JIGoV4yzHxJWHkP_yOXgwsaf1c3hGebBDQ'
START_LAT = 17.5449
START_LNG = 78.5718
DEST_LAT = 17.2403
DEST_LNG = 78.4294
VIA_LAT = 17.4033
VIA_LNG = 78.4707

nodes_counter = {}

via_list = [
    (17.4404, 78.4877),
    (17.4791, 78.3902),
    (17.4011, 78.5591),
    (17.5223, 78.4472),
    (17.5039, 78.5138),
    (17.4004, 78.5481),
    (17.3447, 78.5564),
    (17.2615, 78.498),
    (17.4145, 78.6808),
    (17.3705, 78.5574),
    (17.5383, 78.2369),
    (17.4836, 78.5639),
    (17.4941, 78.3181),
    (17.2897, 78.5502),
]

MODES = ['car', 'pedestrian', 'truck']

URL = 'https://router.hereapi.com/v8/routes?transportMode=car&origin={},{}&destination={},{}&return=polyline&apikey={}'
URL = URL.format(START_LAT, START_LNG, DEST_LAT, DEST_LNG, API_KEY)

URL_VIA = 'https://router.hereapi.com/v8/routes?transportMode=car&origin={},{}&destination={},{}&via={},{}&return=polyline&apikey={}'
# URL_VIA = URL_VIA.format(START_LAT, START_LNG, DEST_LAT, DEST_LNG, VIA_LAT, VIA_LNG, API_KEY)

HYD_LAT = "17.3850"
HYD_LNG = "78.4867"
gmap = gmplot.GoogleMapPlotter(HYD_LAT, HYD_LNG, 11)
gmap.marker(float(START_LAT), float(START_LNG))
gmap.marker(float(DEST_LAT), float(DEST_LNG))


for via in via_list:
    gmap.marker(via[0], via[1], 'blue')

colors = [
    'aliceblue', 
    'antiquewhite', 
    'aqua', 
    'aquamarine', 
    'azure', 
    'beige', 
    'bisque', 
    'black', 
    'blanchedalmond', 
    'blue', 
    'blueviolet', 
    'brown', 
    'burlywood', 
    'cadetblue', 
    'chartreuse', 
    'chocolate', 
    'coral', 
    'cornflowerblue', 
    'cornsilk', 
    'crimson', 
    'cyan', 
    'darkblue', 
    'darkcyan', 
    'darkgoldenrod', 
    'darkgray', 
    'darkgreen', 
    'darkkhaki', 
    'darkmagenta', 
    'darkolivegreen', 
    'darkorange', 
    'darkorchid', 
    'darkred', 
    'darksalmon', 
    'darkseagreen', 
    'darkslateblue', 
    'darkslategray', 
    'darkturquoise', 
    'darkviolet', 
    'deeppink', 
    'deepskyblue', 
    'dimgray', 
    'dodgerblue', 
    'firebrick', 
    'floralwhite', 
    'forestgreen', 
    'fuchsia', 
    'gainsboro', 
    'ghostwhite', 
    'gold', 
    'goldenrod', 
    'gray', 
    'green', 
    'greenyellow', 
    'honeydew', 
    'hotpink', 
    'indianred', 
    'indigo', 
    'ivory', 
    'khaki', 
    'lavender', 
    'lavenderblush', 
    'lawngreen', 
    'lemonchiffon', 
    'lightblue', 
    'lightcoral', 
    'lightcyan', 
    'lightgoldenrodyellow', 
    'lightgray', 
    'lightgreen', 
    'lightpink', 
    'lightsalmon', 
    'lightseagreen', 
    'lightskyblue', 
    'lightslategray', 
    'lightsteelblue', 
    'lightyellow', 
    'lime', 
    'limegreen', 
    'linen', 
    'magenta', 
    'maroon', 
    'mediumaquamarine', 
    'mediumblue', 
    'mediumorchid', 
    'mediumpurple', 
    'mediumseagreen', 
    'mediumslateblue', 
    'mediumspringgreen', 
    'mediumturquoise', 
    'mediumvioletred', 
    'midnightblue', 
    'mintcream', 
    'mistyrose', 
    'moccasin', 
    'navajowhite', 
    'navy', 
    'oldlace', 
    'olive', 
    'olivedrab', 
    'orange', 
    'orangered', 
    'orchid', 
    'palegoldenrod', 
    'palegreen', 
    'paleturquoise', 
    'palevioletred', 
    'papayawhip', 
    'peachpuff', 
    'peru', 
    'pink', 
    'plum', 
    'powderblue', 
    'purple', 
    'red', 
    'rosybrown', 
    'royalblue', 
    'saddlebrown', 
    'salmon', 
    'sandybrown', 
    'seagreen', 
    'seashell', 
    'sienna', 
    'silver', 
    'skyblue', 
    'slateblue', 
    'slategray', 
    'snow', 
    'springgreen', 
    'steelblue', 
    'tan', 
    'teal', 
    'thistle', 
    'tomato', 
    'turquoise', 
    'violet', 
    'wheat', 
    'white', 
    'whitesmoke', 
    'yellow', 
    'yellowgreen', 
]

def distance(a, b):
    p1, p2 = a
    p3, p4 = b
    return math.sqrt(((p3 - p1) ** 2) + ((p4 - p2) ** 2))

graph = {}

for index, via in enumerate(via_list):
    print("Calculating path via: ", via)
    lat, lng = via
    temp_url = URL_VIA.format(START_LAT, START_LNG, DEST_LAT, DEST_LNG, lat, lng, API_KEY)

    r = requests.get(temp_url)
    print("Path calculated, drawing on map...")
    # print(r.json())
    polyline1 = r.json()["routes"][0]["sections"][0]["polyline"]
    polyline2 = r.json()["routes"][0]["sections"][1]["polyline"]
    coordinates_list1 = fp.decode(polyline1)
    coordinates_list2 = fp.decode(polyline2)

    # reducing graph size
    temp_list1 = []
    temp_list2 = []
    temp_list1.append(coordinates_list1[0])
    temp_list2.append(coordinates_list2[0])

    for cood in coordinates_list1:
        if distance(cood, temp_list1[-1]) >= 0.01:
            temp_list1.append(cood)
    
    for cood in coordinates_list2:
        if distance(cood, temp_list2[-1]) >= 0.01:
            temp_list2.append(cood)

    coordinates_list1 = temp_list1
    coordinates_list2 = temp_list2

    coordinates = coordinates_list1 + coordinates_list2
    coordinates = [(START_LAT, START_LNG)] + coordinates + [(DEST_LAT, DEST_LNG)]
    for i, node in enumerate(coordinates):
        coordinates[i] = (round(node[0], 4), round(node[1], 4))
        

    print("# Nodes: ", len(coordinates))

    for node in (coordinates):
        if nodes_counter.get(node) != None:
            nodes_counter[node] += 1
        else:
            nodes_counter[node] = 1

    for i, node in enumerate(coordinates):
        if (i != len(coordinates) - 1 and node != coordinates[i + 1]):
            if (graph.get(node) == None):
                graph[node] = {coordinates[i + 1]}
            else:
                graph[node].add(coordinates[i + 1])



    lat_list1, lng_list1 = zip(*coordinates_list1)
    lat_list2, lng_list2 = zip(*coordinates_list2)
    gmap.plot(lat_list1, lng_list1, 'blue', edge_width=10)
    gmap.plot(lat_list2, lng_list2, 'blue', edge_width=10)

# print(nodes_counter)
# pprint.pprint(graph)
print("total number of nodes: ", len(nodes_counter))
# gmap.draw("my_map.html")

# generating distance matrix now

coordinates = []
for key, value in nodes_counter.items():
    coordinates.append(key)
print("# Unique nodes: ", len(coordinates))

DM_URL = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={}"

INFINITY = 10000000



distance_matrix = {}

for i in range(0, len(coordinates), 1000):

    param = {}
    param["destinations"] = [{"latitude": float(DEST_LAT), "longitude": float(DEST_LNG)}]
    param["origins"] = []
    param["travelMode"] = "driving"

    for j in range(i, min(i + 1000, len(coordinates))):
        param["origins"].append({"latitude": coordinates[j][0], "longitude": coordinates[j][1]})
    
    pprint.pprint(param)
    temp_url = DM_URL.format(env.BING_KEY)
    res = requests.post(temp_url, json.dumps(param))
    print(res.text)
    data = res.json()
    for dist in data['resourceSets'][0]['resources'][0]['results']:
        node = dist['originIndex']
        # dist_travel = dist['travelDistance']
        dist_travel = dist['travelDuration']
        print("node: {}, dist: {}".format(node, dist_travel))

        if (dist_travel == -1):
            dist_travel = INFINITY
        pos = i + node
        distance_matrix[coordinates[node]] = dist_travel


# print(distance_matrix)


def h_dist_dest(a):

    if distance_matrix.get(a) != None:
        return distance_matrix[a]
    return INFINITY


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