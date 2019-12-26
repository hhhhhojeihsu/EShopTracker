#!/usr/bin/env python3

import argparse

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


def main():
  # Parse arugment
  args = parsearg()

if __name__ == '__main__':
  main()
