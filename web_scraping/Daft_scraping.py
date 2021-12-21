import re
from bs4 import BeautifulSoup
import requests
from csv import writer
import numpy as np
import random

url_base = "https://www.daft.ie/property-for-sale/dublin-city?pageSize=20&from="
with open('housing.csv', 'w', encoding='utf8', newline='') as f:
        thewriter = writer(f, delimiter = ';')
        header = ['Location', 'Price', 'Area', 'Beds', 'Baths', 'DistHosp', 'DistSchool', 'DistMarket']
        thewriter.writerow(header)
url = url_base+str(0)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
num_prop_class   = soup.find_all('h1', class_ = "styles__SearchH1-sc-1t5gb6v-3 drATlb")
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

for i in range(0, page_count, 20):
    url = url_base+str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # cls1 = r'Card__CardWrapper-x1sjdn-0 gnintI'
    # cls2 = r'Card__ContentWrapper-x1sjdn-1 jZapEw'
    lists1 = soup.find_all('div', class_="Card__ContentWrapper-x1sjdn-1 jZapEw")
    lists2 = soup.find_all('div', class_="Card__CardWrapper-x1sjdn-0 gnintI")
    lists = lists1 if lists1 != [] else lists2

    with open('housing.csv', 'a', encoding='utf8', newline='') as f:
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

            info = [address[0],# if address != [] else np.nan,
                    re.sub(r"[^0-9 ]", "", price[0]),# if price != [] else np.nan,
                    area[0],# if area != [] else np.nan,
                    beds[0],# if beds != [] else np.nan,
                    baths[0],# if baths != [] else np.nan,
                    random.randint(0, 10),
                    random.randint(0, 10),
                    random.randint(0, 10)]
            thewriter.writerow(info)
