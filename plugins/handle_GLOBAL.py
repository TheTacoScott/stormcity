import re
import sys
try:
  import lib
except:
  pass
import json
import requests
from bs4 import BeautifulSoup as BS
lib.good_mode = True
try:
  from selenium import webdriver
except:
  lib.good_mode = False

def handle(url):
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'} 
  return_data = {"plugin": __name__,"status":0,"type":0,"subdata":{}}
  try:
    driver = webdriver.PhantomJS()
  except:
    lib.good_mode = False
  if lib.good_mode:
    return_data["plugin-type"] = "Selenium with PhantomJS"
  else:
    return_data["plugin-type"] = "Requests"
  return return_data


if __name__ == "__main__":
  print(json.dumps(handle(sys.argv[1]),indent=4))
else:
  lib.url_handlers["GLOBAL"] = handle
