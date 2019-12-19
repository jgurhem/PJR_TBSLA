import argparse

def get_common():
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('-f', '--filter', type=str, action='append', dest='filter_list')
  parser.add_argument('input', help='input file')
  return parser
  
def get_show():
  parser = argparse.ArgumentParser(add_help=False)
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-s', '--show', type=str, action='append', dest='show')
  group.add_argument('-ns', '--not-show', type=str, action='append', dest='not_show')
  return parser

