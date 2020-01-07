#!/usr/bin/env python3
import sys
import requests

## Telegram
BOT_TOKEN = "12345:somerandomstring" # The token acquired from telegram @BotFather
CHAT_ID = "-123456789" # Chat that is group/channel/pm that the bot has access to

def main():
  if(len(sys.argv) != 4):
    sys.exit(1)
  item = sys.argv[1]
  threshold = sys.argv[2]
  current = sys.argv[3]
  text = "Price for '{}' has reached the threshold ({}) you set. Current price is {}".format(item, threshold, current)

  with requests.session as s:
    s.get("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + text)


if __name__ == '__main__':
  main()
