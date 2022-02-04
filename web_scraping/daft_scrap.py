import re
from bs4 import BeautifulSoup
import requests
from csv import writer
import numpy as np
import random

from requests import api
from distance import distance_class

def distance_api(address, dest):
    i = distance_class(api_key = api_key, address_or_postal_code=address)
    obj = i.search(search = dest)
    dist = i.distance_two_points(i.place_id, i.obj_place_id)
    return dist

def find_coordinates(address):
    i = distance_class(api_key=api_key, address_or_postal_code=address)
    _, lat, lng = i.extract_place_id()
    return lat, lng


url_base = "https://www.daft.ie/property-for-sale/dublin-city?pageSize=20&from="
with open('housing_2.csv', 'w', encoding='utf8', newline='') as f:
        thewriter = writer(f, delimiter = ';')
        header = ['Location', 'Price', 'Area', 'Beds', 'Baths', 'DistHosp', 'DistSchool', 'DistMarket', 'lat', 'lng']
        thewriter.writerow(header)
url = url_base+str(0)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
num_prop_class   = soup.find_all('h1', class_ = "styles__SearchH1-sc-1t5gb6v-3 bekXMP")
num_prop_pattern = re.compile(r'.([\d,]*)\sP')
num_prop = re.findall(num_prop_pattern, str(num_prop_class))
tot_prop = re.sub(r"[^0-9 ]", "", num_prop[0])
page_count = (int(tot_prop)//20)*20

price_pattern = re.compile(r'price.{18}[a-z\sA-Z0-9_-]*">[\w\s]*.([\d,]*)')
address_pattern = re.compile(r'address..([a-z,A-Z0-9\s.\(\)\']*)<.*')
bed_pattern = re.compile(r'beds..(\d*)')
baths_pattern = re.compile(r'baths..(\d*)')
# area_pattern = re.compile(r'area..([0-9\sa-z]*)')
area_pattern = re.compile(r'area..([0-9]*)')


school = 'school'
hosp = 'hospital'
shop = 'grocery'

for i in range(0, page_count, 20):
    url = url_base+str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # cls1 = r'Card__CardWrapper-x1sjdn-0 gnintI'
    # cls2 = r'Card__ContentWrapper-x1sjdn-1 jZapEw'
    lists1 = soup.find_all('div', class_="Card__TitleBlockWrapper-x1sjdn-4 dzzYvA")
    lists2 = soup.find_all('div', class_="Card__CardWrapper-x1sjdn-0 gnintI")
    lists = lists1 if lists1 != [] else lists2

    with open('housing_2.csv', 'a', encoding='utf8', newline='') as f:
        # thewriter = writer(f)
        thewriter = writer(f, delimiter = ';')
        for rec in lists:
            price = re.findall(price_pattern, str(rec))
            address = re.findall(address_pattern, str(rec))
            beds = re.findall(bed_pattern, str(rec))
            baths = re.findall(baths_pattern, str(rec))
            area = re.findall(area_pattern, str(rec))
            if beds == [] or baths == [] or price == [] or address == [] or area == [] or price == [''] :  # multiple property within this property
                continue
            dist_school = distance_api(address, school)
            dist_hosp = distance_api(address, hosp)
            dist_market = distance_api(address, shop)
            lat, lng = find_coordinates(address=address)
            info = [address[0],# if address != [] else np.nan,
                    re.sub(r"[^0-9 ]", "", price[0]),# if price != [] else np.nan,
                    area[0],# if area != [] else np.nan,
                    beds[0],# if beds != [] else np.nan,
                    baths[0],# if baths != [] else np.nan,
                    dist_hosp,
                    dist_school,
                    dist_market,
                    lat,
                    lng]
            thewriter.writerow(info)
