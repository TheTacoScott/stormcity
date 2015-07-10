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
  return_data = {"status":0,"type":0,"data":{}}
  result = re.match("^(?:http)s?://shop.nordstrom.com/([a-zA-Z])/([^\?]*)(.*)",url)
  if result:
    if result.group(1) == "c":
      return_data["type"] = 0
      return_data["data"]["items"] = []
      return_data["data"]["category"] = result.group(2)
      r = requests.get(url,headers=headers)
      return_data["data"]["statuscode"] = r.status_code
      soup = BS(r.text, 'html.parser')
      for i in soup.find_all(class_="fashion-results"):
        for x in i.find_all(class_="fashion-item"):
          item_details = {}
          item_details["name"] = x.find(id="ada-title").text
          item_details["price"] = x.find(class_="price").text
          item_details["imgurl"] = x.find("img").attrs["data-original"]
          return_data["data"]["items"].append(item_details)
    elif result.group(1) == "s":
      return_data["type"] = 1
    else:
      return_data["status"] = 1
      return_data["type"] = -1
     
  return return_data


if __name__ == "__main__":
  print(json.dumps(handle(sys.argv[1]),indent=4))
else:
  try:
    lib.url_handlers["shop.nordstrom.com"] = handle
  except:
    pass
