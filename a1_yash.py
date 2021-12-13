import re

class marriage_records:

    def __init__(self, name, area, year, quarter, vol, page):
        self.name = name
        self.area = area
        self.year = year  # return year
        self.quarter = quarter
        self.vol = vol
        self.page = page


with open('C:\\Users\\yashg\\Documents\\UCC\Sem-2\\CS6507\\Assignment-1\\mary_roche.txt') as f:
    mary_content = f.read()

with open('C:\\Users\\yashg\\Documents\\UCC\\Sem-2\\CS6507\\Assignment-1\\nicholas.txt') as f:
    nich_content = f.read()

def save_file(file_mary, file_nich):

    mary_pattern = re.compile(r'[a-zA-z\s]*(MARY .*ROCHE)\s?[a-zA-z]*\s[a-zA-Z0-9\s\/]{66}([^\n]*)\s[A-Za-z\s]*(\d+)\s[A-Za-z\s]*(\d+)\s[A-Za-z\s]*(\d+)\s[A-Za-z\s]*(\d+)')
    nich_pattern = re.compile(r'[a-zA-z\s]*(NICHOLAS .*)\s?[a-zA-z]*\s[a-zA-Z0-9\s\/]{52}([^\n]*)\s[A-Za-z\s]*(\d+)\s[A-Za-z\s]*(\d+)\s[A-Za-z\s]*(\d+)\s[A-Za-z\s]*(\d+)')
    mary_matches = re.findall(mary_pattern, file_mary)
    nich_matches = re.findall(nich_pattern, file_nich)
    obj_mary = [marriage_records(*i) for i in mary_matches]
    obj_nich = [marriage_records(*i) for i in nich_matches]

    for i in obj_nich:
        for j in obj_mary:
            if (i.area, i.year, i.quarter, i.page) == (j.area, j.year, j.quarter, j.page):
                print(r'Possible match!')
                print(f'{i.name} and {j.name} in {i.area} in {i.year} Quarter {i.quarter} , Volume {i.vol}, Page {i.page}\n\n')

save_file(mary_content, nich_content)