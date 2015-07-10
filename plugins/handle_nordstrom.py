import re
import lib
import json
import requests
from bs4 import BeautifulSoup as BS

def handle(url):  
  return_data = {"status":0,"type":0,"data":{}}
  result = re.match("^(?:http)s?://shop.nordstrom.com/([a-zA-Z])/([^\?]*)(.*)",url)
  if result:
    if result.group(1) == "c":
      return_data["type"] = 0
    elif result.group(1) == "s":
      return_data["type"] = 1
    else:
      return_data["status"] = 1
      return_data["type"] = -1
  
    return return_data


lib.url_handlers["shop.nordstrom.com"] = handle
