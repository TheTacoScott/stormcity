import re
import sys
import math
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
  screen_x = 1200
  screen_y = 1000
  screen_pixels = screen_x * screen_y

  def center(element):
    x = (element.location["x"] + (element.size["width"] / 2))
    y = (element.location["y"] + (element.size["height"] / 2))
    return (x,y) 

  def get_info(i):
    temp_loc = i.location
    x = temp_loc["x"]
    y = temp_loc["y"]

    temp_size = i.size
    w = temp_size["width"]
    h = temp_size["height"]

    cx = x + (w / 2)
    cy = y + (h / 2)

    pixels = w * h

    return (x,y,w,h,cx,cy,pixels)

  def distance(e1x,e1y,e2x,e2y):
    e1diffsq = (e2x - e1x)**2
    e2diffsq = (e2y - e1y)**2
    return math.sqrt(e1diffsq + e2diffsq)

  def percent_of_screen(element):
    return float(float(pixels/screen_pixels) * 100.00)


  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'} 
  return_data = {"plugin": __name__,"status":0,"type":0,"subdata":{}}
  try:
    driver = webdriver.PhantomJS()
  except:
    lib.good_mode = False
  if lib.good_mode:
    return_data["plugin-type"] = "Selenium with PhantomJS"
    driver.set_window_size(screen_x, screen_y)
    driver.get(url)

    image_tops = {}
    image_lefts = {}

    links_with_images = []
    money_elements = []

    #http://stackoverflow.com/questions/2150205/can-somebody-explain-a-money-regex-that-just-checks-if-the-value-matches-some-pa

    #find all links that contain an image where the link area is greater than 3% of screen pixels
    money = re.compile('|'.join([r'^\$?(\d*\.\d{1,2})$', r'^\$?(\d+)$',r'^\$(\d+\.?)$'])) 
    for i in driver.find_elements_by_xpath("//a[img]"):
      (x,y,w,h,cx,cy,pixels) = get_info(i)
      if  percent_of_screen(i) > 3:
        links_with_images.append((i,x,y,w,h,cx,cy,pixels,i.get_attribute('href')))
    
    #find all text elements that contain a dollar amount where the area is less than 3% of screen pixels
    for i in driver.find_elements_by_xpath("//*[text()[contains(.,'$')]]"):
      test = money.match(i.get_attribute('innerHTML').strip())
      if test:
        (x,y,w,h,cx,cy,pixels) = get_info(i)
        if percent_of_screen(pixels) < 3:
          money_elements.append((i,x,y,w,h,cx,cy,pixels,test.group(1)))

    #not the best big O    
    return_data["subdata"]["items"] = []
    for (i1,x1,y1,w1,h1,cx1,cy1,pixels1,url) in links_with_images:
      closest_element = None
      closest_element_distance = -1
      closest_element_size = -1
      closest_element_amount = -1
      for (i2,x2,y2,w2,h2,cx2,cy2,pixels2,amount) in money_elements:
        current_distance = distance(x1,y1,x1,y2)
        if closest_element is None:
          closest_element = i2
          closest_element_distance = current_distance
          closest_element_size = pixels2
          closest_element_amount = amount
        else:
          if distance(x1,y1,x1,y2) < closest_element_distance:
            closest_element = i2
            closest_element_distance = current_distance
            closest_element_size = pixels2
            closest_element_amount = amount
          elif distance(x1,y1,x1,y2) == closest_element_distance:
            if pixels2 > closest_element_size:
              closest_element = i2
              closest_element_distance = current_distance
              closest_element_size = pixels2
              closest_element_amount = amount
      return_data["subdata"]["items"].append({"url":url,"best-guess-price":closest_element_amount})
      print("Closest Dollar Amount for:",url,"is",closest_element_amount,"@",closest_element_distance,"size",closest_element_size)
      

    
  
  else:
    return_data["plugin-type"] = "Requests"
  return return_data


if __name__ == "__main__":
  print(json.dumps(handle(sys.argv[1]),indent=4))
else:
  lib.url_handlers["GLOBAL"] = handle
