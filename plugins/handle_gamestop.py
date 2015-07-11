import re
import sys
try:
  import lib
except:
  pass
import json
import requests
from bs4 import BeautifulSoup as BS



def handle(url):
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'} 
  return_data = {"plugin": __name__,"status":0,"type":0,"subdata":{}}
  result = re.match("^.*www.gamestop.com/(.*)",url)
  if result:
    pass
  return return_data


if __name__ == "__main__":
  print(json.dumps(handle(sys.argv[1]),indent=4))
else:
  try:
    lib.url_handlers["www.gamestop.com"] = handle
  except:
    pass
