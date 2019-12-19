import sys
import pjr.DictHelper as dh
import argparse
import common.parser as cp
import common.properties as prop

parser = argparse.ArgumentParser(parents=[cp.get_common(), cp.get_show()])
args = parser.parse_args()

filter_dict = dh.convert_filter_list_to_dic(args.filter_list)
input_res = dh.read_json_file(args.input, filter_dict, "val", prop.CASE_INFO, prop.VALUE_INFO)

for d in input_res:
  new_d = dict()
  for k, v in d.items():
    if args.not_show != None and k in args.not_show: continue
    if args.show != None and k not in args.not_show: continue
    new_d[k] = v
  print(new_d)
