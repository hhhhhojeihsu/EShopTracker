#!/usr/bin/env python3

import argparse
import configparser
import sys

def parsearg():
  argparser_ = argparse.ArgumentParser(prog='EshopTracker',
                                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  argparser_.add_argument('-c', '--config',
                          default='eshop.conf',
                          help='config file')
  argparser_.add_argument('-i', '--interval',
                          type=int,
                          default=12,
                          help='check interval in hour')
  argparser_.add_argument('-n', '--notifier',
                          help='external program to notify user',
                          required=True)

  return argparser_.parse_args()

def parseconf(filename):
  config_ = configparser.RawConfigParser()
  config_.optionxform = str
  if(len(config_.read(filename)) != 1):
    print("Cannot read config file '{}'".format(filename), file=sys.stderr)
    sys.exit(1)
  result = dict()
  for shop in config_.sections():
    result.update({shop: {item: {"url": attribute.split()[0], "target": attribute.split()[1]}} for item, attribute in config_.items(shop)})
  return result

def main():
  # Parse arugment
  args = parsearg()

  # Parse config file
  configs = parseconf(args.config)

if __name__ == '__main__':
  main()
