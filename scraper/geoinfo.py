import urllib.parse
import re
import requests
import time

import config

GEOAPIKEY=config.get('GEOAPIKEY')
CITIES=config.get('CITIES')

def loadCities():
  cities = {}
  with open(CITIES, 'r') as csv:
    l = csv.readline()
    while l:
      val = l.strip().split(';')
      lat=0
      lon=0
      try:
        lat = float(val[2])
        lon = float(val[3])
      except ValueError as e:
        print('Invalid lat/lon', val)
        pass
      cities[val[1]] = {
        'name': val[0],
        'zip': val[1],
        'lat': lat,
        'lon': lon
      }
      l = csv.readline()
  return cities

def __fetchLocation(zipcode, city):
  time.sleep(1.2)
  urlloc = urllib.parse.quote(f'{zipcode} {city}')
  url = f"https://geocode.maps.co/search?q={urlloc}&api_key={GEOAPIKEY}"
  r = requests.get(url)
  data = r.json()
  if len(data) > 0:
    val = data[0]
    with open(CITIES, 'a') as csv:
      csv.write(f"{city};{zipcode};{val['lat']};{val['lon']}\n")
    return {
      'name': city,
      'zip': zipcode,
      'lat': float(val['lat']),
      'lon': float(val['lon'])
    }
  print('Not found', zipcode, city, data)
  if city:
    return __fetchLocation(zipcode, None)
  return None

pcity = re.compile('([0-9]+)\\s+(\\w.+)')
def getLocation(loc, cities):
  m = pcity.match(loc)
  res = None
  if m:
    z = m.group(1)
    name = m.group(2)
    res = cities.get(z)
    if res is None:
      res = __fetchLocation(z, name)
  return res
