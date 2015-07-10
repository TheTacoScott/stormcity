import re
import lib
import json
import requests


def handle(url):
  print("KJHGDFJFGJH:" + url)


lib.url_handlers["shop.nordstrom.com"] = handle
