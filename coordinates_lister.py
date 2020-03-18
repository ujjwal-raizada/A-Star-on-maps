import env
import requests
import json
import pickle

landmark_list = [
    'Ananda Buddha Vihara',
    'Apollo Hospital Hyderabad',
    'Ashtalakshmi Temple',
    'Asian Institute of Gastroenterology',
    'Char Minar',
    'Chilkur Balaji Temple',
    'Chowmahalla Palace',
    'City Center Mall',
    'Fernandez Hospital',
    'Golconda Fort',
    'Hussain Sagar Lake',
    'Hyderabad Central Mall',
    'Hyderabad Deccan Railway Station',
    'Inorbit Mall Hyderbad',
    'Mecca Masjid',
    'Necklace Road',
    'Nehru Zoological Park',
    'Nizam\'s Institute of Medical Sciences',
    'Qutb Shahi Tombs',
    'Qutub Shahi Tombs',
    'Rajiv Gandhi International Airport',
    'Ramoji Film City',
    'Salar Jung Museum',
    'Secunderabad Junction Railway Station',
    'Sri Lakshminarasimha Swamy Temple',
    'St. Joseph\'s Cathedral Hyderabad',
]

coordinates_list = {}
URL = "http://dev.virtualearth.net/REST/v1/Locations/{}?key={}&o=json"


for place in landmark_list:
    query = place.replace(' ', '%20')
    URL_coded = URL.format(query, env.BING_KEY)
    print("place: ", place)
    print("URL: ", URL_coded)
    res = requests.get(URL_coded)
    data = (res.json())
    name = data['resourceSets'][0]['resources'][0]['name']
    coordinates = data['resourceSets'][0]['resources'][0]['point']['coordinates']
    print("name: ", name)
    print("coordinates: ", coordinates)
    print()
    coordinates_list[place] = coordinates

print("final list: ", coordinates_list)
dbfile = open('coordinates_list_db', 'ab+') 
pickle.dump(coordinates_list, dbfile)



