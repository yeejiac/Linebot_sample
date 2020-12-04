import googlemaps
import os
import sys
parent_dir = os.path.dirname(sys.path[0])
sys.path.insert(0, parent_dir)
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數哦！

def get_nearby_restaurant(lon, lat):
    GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
    gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    location = (25.017156, 121.506359)
    radius = 500
    place_type = 'restaurant'
    places_radar_result = gmaps.places_nearby(location, radius, type=place_type)
    urlstring = ['https://www.google.com/maps/place/?q=place_id:'+i['place_id'] for i in places_radar_result['results']]
    # print(urlstring)
    return urlstring


# if __name__ == '__main__':
#     get_nearby_restaurant(25.042363209943446, 121.56481611369205)