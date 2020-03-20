from math import radians, cos, sin, asin, sqrt
import heapq, pickle

# we will use haversine distance as the hurestic value between two points,
# as euclidean distance doesn't make sense due to curved surface of earth.

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

dbfile = open('coordinates_index_db', 'rb') 
coordinates_index = pickle.load(dbfile)
dbfile.close()

dbfile = open('distance_matrix_db', 'rb') 
distance_matrix = pickle.load(dbfile)
dbfile.close()


def a_star(distance_matrix, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    open_list = []
    heapq.heapify(open_list)
    closed_list = []

    heapq.heappush(open_list, (0, start, 0))

    while len(open_list) > 0:

        current_node = heapq.heappop(open_list)
        print(current_node)
        closed_list.append(current_node[1])

        if current_node[1] == end:
            print('found')

        children = [x for x in range(0, 26)]
        print("children: ", children)

        for child in children:

            if child in closed_list:
                continue

            g_value = current_node[2] + distance_matrix[(child, current_node[1])][0]
            h_value = haversine(coordinates_index[child][0], coordinates_index[child][1], coordinates_index[end][0], coordinates_index[end][1])
            f_value = g_value + h_value

            flag = 0
            for node in open_list:
                if node[1] == child:
                    flag = 1

            if flag == 1:
                continue
            heapq.heappush(open_list, (f_value, child, g_value))


a_star(distance_matrix, 0, 1)