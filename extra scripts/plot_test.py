import requests
import flexpolyline as fp
from gmplot import gmplot


API_KEY = '4A-Ns4qs8JIGoV4yzHxJWHkP_yOXgwsaf1c3hGebBDQ'
START_LAT = '17.5449'
START_LNG = '78.5718'
DEST_LAT = '17.2403'
DEST_LNG = '78.4294'
VIA_LAT = '17.4033'
VIA_LNG = '78.4707'


MODES = ['car', 'pedestrian', 'truck']

URL = 'https://router.hereapi.com/v8/routes?transportMode=car&origin={},{}&destination={},{}&return=polyline&apikey={}'
URL = URL.format(START_LAT, START_LNG, DEST_LAT, DEST_LNG, API_KEY)

URL_VIA = 'https://router.hereapi.com/v8/routes?transportMode=car&origin={},{}&destination={},{}&via={},{}&return=polyline&apikey={}'
URL_VIA = URL_VIA.format(START_LAT, START_LNG, DEST_LAT, DEST_LNG, VIA_LAT, VIA_LNG, API_KEY)

r = requests.get(URL)
print(r.json())
polyline = r.json()["routes"][0]["sections"][0]["polyline"]
coordinates_list = fp.decode(polyline)

lat_list, lng_list = zip(*coordinates_list)

HYD_LAT = "17.3850"
HYD_LNG = "78.4867"
gmap = gmplot.GoogleMapPlotter(HYD_LAT, HYD_LNG, 11)

gmap.marker(float(START_LAT), float(START_LNG))
gmap.marker(float(DEST_LAT), float(DEST_LNG))
gmap.plot(lat_list, lng_list, edge_width=10)
gmap.draw("my_map.html")

