import googlemaps
import os
import sys
parent_dir = os.path.dirname(sys.path[0])
sys.path.insert(0, parent_dir)
import configparser
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)

config = configparser.ConfigParser()
config.read("config.ini")

def get_nearby_restaurant(lon, lat):
    GOOGLE_PLACES_API_KEY = config['Google_API']['GOOGLE_PLACES_API_KEY']
    gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    location = (lon, lat)
    radius = 200
    place_type = 'restaurant'
    places_radar_result = gmaps.places_nearby(location, radius, type=place_type)
    if places_radar_result['status'] == 'OK':
        print(places_radar_result)
        urlstring = ['https://www.google.com/maps/place/?q=place_id:'+i['place_id'] for i in places_radar_result['results']]
        print(urlstring)
        return urlstring
    else:
        return []


if __name__ == '__main__':
    get_nearby_restaurant(25.042363209943446, 121.56481611369205)