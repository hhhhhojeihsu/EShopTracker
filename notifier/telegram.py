#!/usr/bin/env python3
import sys
import requests
import os

## Telegram
# "111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" The token acquired from telegram @BotFather
BOT_TOKEN = os.environ['ESHOP_TG_BOT_TOKEN']
# "-111111111" Chat that is group/channel/pm that the bot has access to
CHAT_ID = os.environ['ESHOP_TG_CHAT_ID']

def main():
  if(len(sys.argv) == 1):
    text = "Exception occurred, program update required"
  elif(len(sys.argv) == 4):
    item = sys.argv[1]
    threshold = sys.argv[2]
    current = sys.argv[3]
    text = "Price for '{}' has reached the threshold ({}) you set. Current price is {}".format(item, threshold, current)

  with requests.session() as s:
    s.get("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + text)


if __name__ == '__main__':
  main()
