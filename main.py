#!/usr/bin/env python3

from apscheduler.schedulers.blocking import BlockingScheduler
import argparse
import configparser
import sys
import importlib
import subprocess

def parsearg():
  argparser_ = argparse.ArgumentParser(prog='EshopTracker',
                                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  argparser_.add_argument('-c', '--config',
                          default='eshop.conf',
                          help='config file')

  return argparser_.parse_args()

def parseconf(filename):
  config_ = configparser.RawConfigParser()
  config_.optionxform = str
  if(len(config_.read(filename)) != 1):
    print("Cannot read config file '{}'".format(filename), file=sys.stderr)
    sys.exit(1)

  general = dict(config_['general'])
  if 'interval' and 'notifier' not in general:
    print("'interval' and 'notifier' required in [general] section", file=sys.stderr)
    sys.exit(1)

  result = dict()
  eshops = config_.sections()
  eshops.remove('general')
  for eshop_ in eshops:
    result[eshop_] = dict()
    for item, attribute in config_.items(eshop_):
      result[eshop_].update({item: {"url": attribute.split()[0], "target": attribute.split()[1]}})
  return general, result

def send_notification(path, item, target, current_price, exception=False):
  if(exception):
    subprocess.Popen([path])
  else:
    subprocess.Popen([path, item, str(target), str(current_price)])

def main(configs, item_lists, old_current_price):
  # Get each item's current status
  eshop_module = importlib.import_module("eshop")
  for eshop_ in item_lists:
    eshop_class = getattr(eshop_module, eshop_)
    for item in item_lists[eshop_]:
      eshop_class_ = eshop_class(item, item_lists[eshop_][item]['url'])
      if hasattr(eshop_class_, 'exception'):
        send_notification(configs['notifier'], None, None, None, exception=True)
        continue

      # Update old_current_price
      if item not in old_current_price:
        old_current_price[item] = -1

      # Get original and current price
      current_price = eshop_class_.price
      original_price = eshop_class_.original_price

      # Check if prices has changed
      if old_current_price[item] == current_price:
        continue
      old_current_price[item] = current_price

      # Compare with target
      target = item_lists[eshop_][item]['target']
      if '%' in target:
        if original_price * int(target[:-1]) * 0.01 >= current_price:
          send_notification(configs['notifier'], item, target, current_price)
      else:
        if current_price <= int(target):
          send_notification(configs['notifier'], item, target, current_price)

if __name__ == '__main__':
  # Parse arugment
  args = parsearg()

  # Parse config file
  configs, item_lists = parseconf(args.config)

  old_current_price = dict()

  main(configs, item_lists, old_current_price)
  scheduler = BlockingScheduler()
  scheduler.add_job(main, 'interval', hours=int(configs['interval']), args=[configs, item_lists, old_current_price]) # Data may not be updated on time

  scheduler.start()

