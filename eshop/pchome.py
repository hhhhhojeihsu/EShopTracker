import requests_html
from bs4 import BeautifulSoup

class pchome:
  def __init__(self, item, url, target):
    self.result = str()
    with requests_html.HTMLSession() as s:
      try:
        resp = s.get(url)
      except:
        result = "Item {} url {} invalid".format(item, url)
      resp.html.render()
      soup = BeautifulSoup(resp.text, 'html.parser')

