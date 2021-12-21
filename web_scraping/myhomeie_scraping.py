import re
from bs4 import BeautifulSoup
import requests
from csv import writer
import numpy as np
import random

url_base = r'https://www.myhome.ie/residential/dublin/property-for-sale?page='
url = url_base+str(1)
page = requests.get(url)
print(page)
soup = BeautifulSoup(page.content, 'html.parser')
lists1 = soup.find_all('div', class_="PropertyListingCard__PropertyInfo")
# print(lists1[0])
with open('home_housing.csv', 'w', encoding='utf8', newline='') as f:
        thewriter = writer(f, delimiter = ';')
        header = ['Location', 'Price', 'Area', 'Beds', 'Baths', 'DistHosp', 'DistSchool', 'DistMarket']
        thewriter.writerow(header)

url = url_base+str(0)
bed_pattern = re.compile(r'\d+\sbed')
bath_pattern = re.compile(r'\d+\sbath')
area_pattern = re.compile(r'\d+\w+\s\<sup')
for i in range(1, 100, 1):
    url = url_base+str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lists1 = soup.find_all('div', class_="PropertyListingCard__PropertyInfo")
    with open('home_housing.csv', 'a', encoding='utf8', newline='') as f:
        # thewriter = writer(f)
        thewriter = writer(f, delimiter = ';')
        for list in lists1:
            price = list.find('div', class_="PropertyListingCard__Price").text.replace('\n', '')
            address = list.find('a', class_="PropertyListingCard__Address").text.replace('\n', '')
            bed = re.findall(bed_pattern, str(list))
            bath = re.findall(bath_pattern, str(list))
            area = re.findall(area_pattern, str(list))
            #print(price, address, bed, bath, area)
            if bed == [] or bath == [] or price == 'POA' or address == [] or area == []:  # multiple property within this property
                continue
            info = [address,# if address != [] else np.nan,
                    re.sub(r"[^0-9 ]", "", price),# if price != [] else np.nan,
                    re.sub(r"[^0-9 mft]", "", area[0]),# if area != [] else np.nan,
                    re.sub(r"[^0-9 ]", "", bed[0]),# if beds != [] else np.nan,
                    re.sub(r"[^0-9 ]", "", bath[0]),# if baths != [] else np.nan,
                    random.randint(0, 10),
                    random.randint(0, 10),
                    random.randint(0, 10)]
            thewriter.writerow(info)

