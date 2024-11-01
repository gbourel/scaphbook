import json
import requests
from bs4 import BeautifulSoup
import os
import time

import config
import geoinfo

DEST=config.get('DESTFILE')

HTML_TTL=12*60*60  # 12h

def extract(cache, url):
  if not os.path.isfile(cache) or (time.time() - os.path.getmtime(cache)) > HTML_TTL:
    print(f'Refresh {cache}')
    r = requests.get(url, auth=('user', 'pass'))
    with open(cache, 'w') as f:
      f.write(r.text)

def scrap(cities, cache, srcurl):
  extract(cache, srcurl)

  with open(cache, 'r') as f:
    soup = BeautifulSoup(f.read(), "html.parser")
    articles = soup.find_all("article")
    res = []
    for r in articles:
      h2 = r.find('h2')
      a = h2.find('a')
      loc = r.find('div', class_='bd-customcmscode-2')
      locdata = geoinfo.getLocation(loc.contents[0].strip(), cities)
      name = a.contents[0]
      logo=None
      img = r.find('img')
      if img:
        logo = img.attrs['src']
      if name:
        name = name.replace('\u2013', '')
        name = name.strip()
      if locdata:
        res.append({
          'name': name,
          'url': a.attrs['href'],
          'loc': locdata,
          'logo': logo
        })
      else:
        print('Location not found', loc.contents[0])
    return res

c = geoinfo.loadCities()

data ={
  "entreprises": scrap(c, "cache/entreprises.html", "https://www.travaux-sous-marins.com/annuaire/les-entreprises/en-france/"),
  "interim": scrap(c, "cache/interim.html", "https://www.travaux-sous-marins.com/annuaire/linterim/"),
  "formation": scrap(c, "cache/formation.html", "https://www.travaux-sous-marins.com/annuaire/la-formation/")
}
with open(DEST, 'w') as jf:
  jf.write(json.dumps(data))
with open('../scaphdata.json', 'w') as jf:
  jf.write(json.dumps(data))
