import requests
import json
import re

class pchome:
  def __init__(self, item, url):
    headers_ = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
               'referer': url
    }
    api_url = url.replace('/prod/', '/ecapi/ecshop/prodapi/v2/prod/') + "&fields=Price&_callback=jsonp_prod"
    with requests.session() as s:
      try:
        resp = s.get(api_url, headers=headers_)
        json_text = re.search(r'jsonp_prod\((.*?)\)', resp.text).group(1)
        item_json = json.loads(json_text)
        if len(item_json) != 1:
          raise exception
        for item_code in item_json:
          self.price = item_json[item_code]["Price"]["P"]
        print(self.price)
      except:
        self.exeception = True

