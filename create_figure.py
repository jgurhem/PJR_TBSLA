import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import sys
import pjr.DBHelper as dh
import pjr.DBRelator as dr
import argparse
import common.parser as cp
import common.properties as prop
import numpy as np

parser = argparse.ArgumentParser(parents=[cp.get_common()])
parser.add_argument('-l', '--list-cases', type=str, help='list of attributes to compare against the case of interest', action='append', dest='list_cases', required=True)
parser.add_argument('-voi', type=str, help='value of interest', dest='voi', required=True)
parser.add_argument('-coi', type=str, help='case of interest', dest='coi', required=True)
parser.add_argument('-o', type=str, help='Name of the output figure file', dest='output', default='output.pdf')
args = parser.parse_args()

filter_dict = dh.convert_filter_list_to_dic(args.filter_list)
case_info = list(args.list_cases)
case_info.append(args.coi)
input_res = dh.read_json_file(args.input, filter_dict, case_info, [args.voi])

for i in prop.CASE_INFO:
  print(i, dh.extract_set(input_res, i))

m, coi_set = dr.matrix_relation(input_res, args.list_cases, args.coi, args.voi, 'auto', 'min')
coi_set = sorted(coi_set, key=float)

fig = plt.figure()
ax = fig.gca()

for k, v in m.items():
  print()
  print(k, v)
  ax.plot(np.arange(len(v.keys())), v.values(), label=str(k).replace("'",''), marker='*')

ax.set_ylabel("Time")
ax.set_xlabel(args.coi)
ax.xaxis.set_ticklabels(coi_set)
ax.xaxis.set_ticks(np.arange(len(coi_set)))

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(args.output, bbox_inches="tight")
plt.close()

