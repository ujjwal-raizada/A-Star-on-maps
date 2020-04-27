import pickle
import json
import requests

import env

URL = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins={}&destinations={}&travelMode=driving&key={}"
INFINITY = 100000

dbfile = open('coordinates_list_db', 'rb') 
coordinates_list = pickle.load(dbfile)
dbfile.close()

print(coordinates_list)

param_co = ""
for key, value in coordinates_list.items():
    param_co += str(value[0]) + "," + str(value[1]) + ";"

print(param_co)
param_co = param_co[:-1]
URL_coded = URL.format(param_co, param_co, env.BING_KEY)
res = requests.get(URL_coded)
data = res.json()
print(json.dumps(res.json(), sort_keys=True, indent=4))

no_of_landmarks = len(coordinates_list)
print("no_of_landmarks: ", no_of_landmarks)
distance_matrix = {}

for pair_distance in data['resourceSets'][0]['resources'][0]['results']:
    node2 = pair_distance['destinationIndex']
    node1 = pair_distance['originIndex']
    distance = pair_distance['travelDistance']
    duration = pair_distance['travelDuration']

    if (distance == -1):
        distance = INFINITY
    
    distance_matrix[(node1, node2)] = (distance, duration)
    distance_matrix[(node2, node1)] = (distance, duration)
    print("({}, {}): {}, {}".format(node1, node2, distance_matrix[(node1, node2)][0], distance_matrix[(node1, node2)][1]))


print("final matrix: ", distance_matrix)
dbfile = open('distance_matrix_db', 'wb+') 
pickle.dump(distance_matrix, dbfile)
dbfile.close()

