import requests
from urllib.parse import urlencode

class distance(object):

    data_type = 'json'
    location_query = None
    api_key = None
    
    def __init__(self, api_key = None, address_or_postal_code = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key == None:
            raise Exception("API key is required")
        self.api_key = api_key
        self.location_query = address_or_postal_code
        if self.location_query != None:
            self.extract_place_id()
        self.place_id,_,_ = self.extract_place_id()
    
    def extract_place_id(self, location = None):
        loc_query = self.location_query
        if location != None:
            loc_query = location
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        params = {
            'address' : loc_query,
            'key' : self.api_key
        }
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        latlng = {}
        if r.status_code not in range(200, 299):
            return {}
        try:
            place_id = r.json()['results'][0]['place_id']
            latlng = r.json()['results'][0]['geometry']['location']
        except:
            pass
        lat,lng = latlng.get("lat"), latlng.get("lng")
        self.lat = lat
        self.lng = lng
        self.place_id = place_id
        return place_id, lat, lng
    
    def search(self, search = None, location  = None):
        lat, lng = self.lat, self.lng
        if search == None:
            raise Exception('search key is required')
        if location != None:
            _,lat, lng = self.extract_place_id(location=location)
        base_endpoint_places = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/{self.data_type}"
        params = {
            'key': self.api_key,
            'input' : search,
            'inputtype' : 'textquery',
            'fields' : 'place_id,name,geometry',  #cannot have spaces in fields
            'locationbias' : f'point:{lat},{lng}'
        }
        params_encoded = urlencode(params)
        places_endpoint = f'{base_endpoint_places}?{params_encoded}'
        r = requests.get(places_endpoint)  
        if r.status_code not in range(200, 299):
            return {}
        try:
            place_id = r.json()['candidates'][0]['place_id']
            name = r.json()['candidates'][0]['name']
        except:
            pass
        self.obj_name = name
        self.obj_place_id = place_id
        return name, place_id

    
    def distance(self, origin_p_id, dest_p_id):
        base_endpoint_dist = f'https://maps.googleapis.com/maps/api/distancematrix/{self.data_type}'
        params = {
            'key' : self.api_key,
            'destinations' : f'place_id:{dest_p_id}',
            'origins' : f'place_id:{origin_p_id}',
            'mode' : 'driving'
        }
        params_encoded = urlencode(params)
        distance_endpoint = f'{base_endpoint_dist}?{params_encoded}'
        r = requests.get(distance_endpoint)
        if r.status_code not in range(200-299):
            return {}
        try:
            distance = r.json()['rows'][0]["elements"][0].get('distance').get('text')
        except:
            pass
        return distance
if __name__ == '__main__':
    with open('api_key.txt') as f:
        api_key = f.read()
    
    api_key = api_key.strip()
    address = '102 Iveragh Road, Whitehall, Whitehall, Dublin 9'
    row1 = distance(api_key = api_key, address_or_postal_code=address)
    obj1 = 'school'
    print(row1.search(search=obj1))      
