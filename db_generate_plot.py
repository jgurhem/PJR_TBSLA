import common.mpl as plot
import pjr.DBRelator as dr
import pjr.DBHelper as dh
import argparse
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list-cases', type=str, help='list of attributes to compare against the case of interest', action='append', dest='list_cases', required=True)
parser.add_argument('-s', '--list-sub-cases', type=str, help='list of attributes to compare against the case of interest', action='append', dest='list_sub_cases', default=list())
parser.add_argument('-voi', type=str, help='value of interest', dest='voi', required=True)
parser.add_argument('-coi', type=str, help='case of interest', dest='coi', required=True)
parser.add_argument('-o', type=str, help='Name of the output figure file', dest='output', default='output.pdf')
parser.add_argument('-pv', help='Print values for the figure', dest='pv', default=False, action='store_true')
parser.add_argument('db_path', help='Path to the database')
parser.add_argument('-p', '--prefix', type=str, help='Prefix for the created tables', dest='prefix', default='auto')
args = parser.parse_args()

dict_cases = dh.convert_filter_list_to_dic(args.list_cases)
con = sqlite3.connect(args.db_path)
m, coi_set = dr.matrix_relation(con, dict_cases, args.list_sub_cases, args.coi, args.voi, args.prefix, ['mean'])
coi_set = sorted(coi_set, key=float)

fig = plot.plot_axis(m, coi_set, 'mean', args.coi, 'Time', args.pv)
plot.save(fig, args.output)

