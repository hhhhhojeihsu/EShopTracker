#!/usr/bin/env python3

import argparse
import configparser
import sys
import importlib

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
  shop_list = config_.sections()
  shop_list.remove('general')
  for shop in shop_list:
    result.update({shop: {item: {"url": attribute.split()[0], "target": attribute.split()[1]}} for item, attribute in config_.items(shop)})
  return general, result

def main():
  # Parse arugment
  args = parsearg()

  # Parse config file
  configs, shops = parseconf(args.config)

  # Get each item's current status
  eshop_module = importlib.import_module("eshop")
  for eshop_ in shops:
    eshop_class = getattr(eshop_module, eshop_)
    for item in shops[eshop_]:
      pass
      #print(eshop_class(item, shops[eshop_][item]['url'], shops[eshop_][item]['target']).result)

if __name__ == '__main__':
  main()

