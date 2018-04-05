from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import json

# import pprint
# pp = pprint.PrettyPrinter(indent=2)

biljac_url_base = 'https://www.bil-jac.com/'
biljac_breed_list = 'dog-breeds.php'

uClient = uReq(biljac_url_base + biljac_breed_list)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

container = page_soup.findAll("div", {"id": "breeds"})[0]

breedList = container.findAll("a")

breedMap = dict()

# map of name of breed to link for information
# eg. Affenpinscher: https://www.bil-jac.com/breed.php?name=Affenpinscher
for breed in breedList:
    breedMap[breed.get_text()] = biljac_url_base + breed.get('href')

# collect data
fact_ids = {
    'size': 'Size: ',
    'weight': 'Weight: ',
    'life': 'Life Span: ',
    'height': 'Height: ',
}

detail_ids = {
    'aka',
    'group',
    'origin',
    'role',
    'history',
    'temperament',
    'health'
}

# the person who made the website misspelled exercise
special_ids = {
    'excercise',
    'grooming'
}

breeds = list()

for breedName, breedLink in breedMap.items():
    print(breedName, breedLink)
    breedClient = uReq(breedLink)
    breed_page = breedClient.read()
    breedClient.close()
    breed_soup = soup(breed_page, "html.parser")

    breed = dict()

    breed['name'] = breedName
    breed['link'] = breedLink

    bc = breed_soup.findAll("div", {"id": "breeddetail"})

    if len(bc) == 0:
        continue

    breed_container = bc[0]
    image_link = breed_container.findAll("img")[0]

    breed['img'] = biljac_url_base + image_link.get('src')

    breed['facts'] = dict()
    for fact, remove in fact_ids.items():
        breed['facts'][fact] = breed_container.findAll("p", {"id": fact})[0].get_text().replace(remove, '')

    details_container = breed_container.findAll("div", {"id": "details"})[0]

    breed['details'] = dict()
    for detail_id in detail_ids:
        breed['details'][detail_id] = details_container.findAll("p", {"id": detail_id})[0].get_text()

    breed['details']['special'] = dict()
    for special_id in special_ids:
        key = 'exercise' if special_id == 'excercise' else special_id
        breed['details']['special'][key] = details_container.findAll("span", {"id": special_id})[0].get_text()

    breeds.append(breed)

with open('dogies.json', 'w') as fp:
    json.dump(breeds, fp, sort_keys=True, indent=2)

