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
  result = re.match("^(?:http)s?://shop.nordstrom.com/([a-zA-Z])/([^\?]*)(.*)",url)
  if result:
    #category page
    if result.group(1) == "c":
      return_data["type"] = 0
      return_data["subdata"]["items"] = []
      return_data["subdata"]["category"] = result.group(2)
      r = requests.get(url,headers=headers)
      return_data["subdata"]["statuscode"] = r.status_code
      soup = BS(r.text, 'html.parser')
      for i in soup.find_all("ul",class_="product-results-pagination"):
        for x in i.find_all("li",class_="page-next"):
          return_data["subdata"]["nexturl"] = x.find("a").get('href')
      for i in soup.find_all(class_="fashion-results"):
        for x in i.find_all(class_="fashion-item"):
          item_details = {}
          item_details["name"] = x.find(id="ada-title").text
          item_details["price"] = x.find(class_="price").text
          item_details["link"] = x.find("a",class_="title").attrs["href"]
          item_details["imgurl"] = x.find("img").attrs["data-original"]
          return_data["subdata"]["items"].append(item_details)
      for i in soup.find_all(id="main-content"):
        for x in i.find_all(class_="product-item"):
          item_details = {}
          item_details["name"] = x.find(class_="product-href").text
          item_details["price"] = x.find(class_="price").text
          item_details["link"] = x.find("a",class_="title").attrs["href"]
          item_details["imgurl"] = x.find("img").attrs["data-original"]
          return_data["subdata"]["items"].append(item_details)
    #product page
    elif result.group(1) == "s":
      return_data["type"] = 1
      r = requests.get(url,headers=headers)
      return_data["subdata"]["statuscode"] = r.status_code
      soup = BS(r.text, 'html.parser')
      return_data["subdata"]["itemnum"] = re.sub("[^0-9]","",soup.find("div",class_="item-number-wrapper").text)
      return_data["subdata"]["title"] = soup.find(id="product-title").find("h1").text
      return_data["subdata"]["brand"] = soup.find(id="brand-title").find("a").text
      return_data["subdata"]["brand-link"] = soup.find(id="brand-title").find("a").get("href")
      return_data["subdata"]["price"] = re.sub("[^0-9\.]","",soup.find(class_="item-price").text)
      if soup.find(class_="sale-price").text:
        return_data["subdata"]["price"] = re.sub("[^0-9\.]","",soup.find(class_="sale-price").text)
      return_data["subdata"]["breadcrumb"] = re.sub("\n","",soup.find(id="breadcrumb-nav").text).split("/")
   
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
