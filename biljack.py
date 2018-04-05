from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pprint

biljac_url_base = 'https://www.bil-jac.com/'
biljac_breed_list = 'dog-breeds.php'

uClient = uReq(biljac_url_base + biljac_breed_list)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

container = page_soup.findAll("div", {"id": "breeds"})[0]

# print(len(container))

breedList = container.findAll("a")

# print(len(breedList))
# print(breedList[0].get_text())
# print(breedList[0].get('href'))

breedMap = dict()

# map of name of breed to link for information
# eg. Affenpinscher: https://www.bil-jac.com/breed.php?name=Affenpinscher
for breed in breedList:
    breedMap[breed.get_text()] = biljac_url_base + breed.get('href')

# print(next(iter(breedMap.values())))

# collect data

fact_ids = {
    'size': 'Size: ',
    'weight': 'Weight: ',
    'life': 'Life Span: ',
    'height': 'Height: ',
}

breeds = list()
pp = pprint.PrettyPrinter(indent=2)

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

    facts = dict()

    for fact, remove in fact_ids.items():
        facts[fact] = breed_container.findAll("p", {"id": fact})[0].get_text().replace(remove, '')

    breed['facts'] = facts

    details_container = breed_container.findAll("div", {"id": "details"})[0]
    details = details_container.findAll("p")
    ds = dict()
    for d in details:
        id = d.get('id')
        if not id:
            id = "special"
        ds[id] = d.get_text()
    breed['details'] = ds
    pp.pprint(breed)
    print("\n")
    breeds.append(breed)

#fil# ename="dogies.json"
#f=open(filename, "w")
