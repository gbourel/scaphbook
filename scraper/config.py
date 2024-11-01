import json
import os

cdata = {}

conf_dir = 'conf'

if os.path.exists(f'{conf_dir}/default.json'):
  with open(f'{conf_dir}/default.json', 'r') as f:
    cdata = json.load(f)
else:
  print('Error loading configuration, default file not found')

if os.path.exists(f'{conf_dir}/local.json'):
  with open(f'{conf_dir}/local.json', 'r') as f:
    local = json.load(f)
    cdata = {**cdata, **local}

def get(*keys):
  if len(keys) < 1:
    return "Missing key."
  cur = cdata
  for key in keys:
    if cur is not None:
      cur = cur.get(key)
  return cur
