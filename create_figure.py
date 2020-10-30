import pjr.DBHelper as dh
import pjr.DBRelator as dr
import argparse
import common.parser as cp
import common.properties as prop
import common.mpl as plot
import common.latex as table

parser = argparse.ArgumentParser(parents=[cp.get_common()])
parser.add_argument('-l', '--list-cases', type=str, help='list of attributes to compare against the case of interest', action='append', dest='list_cases', required=True)
parser.add_argument('-s', '--list-sub-cases', type=str, help='list of attributes to compare against the case of interest', action='append', dest='list_sub_cases', default=list())
parser.add_argument('-r', '--list-ratio-condition', type=str, help='list of ratios the cases have to respect in the from of : param1(str),param2(str),ratio(double) where param1*ratio=param2', action='append', dest='list_ratio', default=list())
parser.add_argument('-voi', type=str, help='value of interest', dest='voi', required=True)
parser.add_argument('-coi', type=str, help='case of interest', dest='coi', required=True)
parser.add_argument('-op', type=str, help='Operation used to compute statistics on the values of the same case (mean, min, max, median, sum, std, var)', dest='op', default='mean')
parser.add_argument('-xlabel', type=str, help='x label', dest='xlabel', default='')
parser.add_argument('-ylabel', type=str, help='y label', dest='ylabel', default='')
parser.add_argument('-grid', type=str, help='Pass grid property to matplotlib \'x\' \'y\' \'both\'', dest='grid', default='')
parser.add_argument('-cpn', type=int, help='number of cores per node', dest='cpn', default=0)
parser.add_argument('-o', type=str, help='Name of the output figure file', dest='output', default='output.pdf')
parser.add_argument('-dbo', type=str, help='Name of the output database file', dest='dbo', default='test.db')
parser.add_argument('-par', help='Print attributes range', dest='par', default=False, action='store_true')
parser.add_argument('-pv', help='Print values for the figure', dest='pv', default=False, action='store_true')
parser.add_argument('-rt', '--rotate-ticks', help='Rotate ticks', dest='rt', default=False, action='store_true')
parser.add_argument('--table', help='Generate Latex table with the results', dest='table', default=False, action='store_true')
args = parser.parse_args()

filter_dict = dh.convert_filter_list_to_dic(args.filter_list)
dict_cases = dh.convert_filter_list_to_dic(args.list_cases)
case_info = list(dict_cases.keys())
case_info.append(args.coi)
for i in args.list_sub_cases:
  case_info.append(i)
input_res = dh.read_json_file(args.dbo, args.input, filter_dict, case_info, [args.voi])

if args.par:
  for i in prop.CASE_INFO:
    print(i, dh.extract_set(input_res, i))

m, coi_set = dr.matrix_relation(input_res, dict_cases, args.list_sub_cases, args.coi, args.voi, 'auto', [args.op], args.list_ratio)
coi_set = sorted(coi_set, key=float)

xlabel = args.xlabel
ylabel = args.ylabel
if xlabel == '':
  xlabel = args.coi
if ylabel == '':
  ylabel = 'Time'
fig = plot.plot_axis(m, coi_set, args.op, xlabel, ylabel, args.pv)
if args.cpn > 0:
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, args.cpn)
if args.grid != '':
  plot.grid(fig, args.grid)

if args.rt:
  plot.rotate_xticks(coi_set)

plot.save(fig, args.output)
if args.table:
  table.table(m, args.output + '.tex')

