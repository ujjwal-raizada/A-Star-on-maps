import pickle

dbfile = open('distance_matrix_db', 'rb') 
distance_matrix = pickle.load(dbfile)
dbfile.close()

dbfile = open('coordinates_list_db', 'rb') 
coordinates_list = pickle.load(dbfile)
dbfile.close()

print(distance_matrix[(0, 0)])
