import pjr.DBHelper as dh
import pjr.DBRelator as dr
import argparse
import common.properties as prop
import common.mpl as plot
import common.cmd as cmd
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file')
parser.add_argument('-par', help='Print attributes range', dest='par', default=False, action='store_true')
parser.add_argument('-pv', help='Print values for the figure', dest='pv', default=False, action='store_true')
parser.add_argument('-db', help='Database file path', dest='db', default='tbsla_pagerank/pagerank_plot.db')
parser.add_argument('-o', help='Output directory path', dest='out', default='tbsla_pagerank/pagerank_plot')
args = parser.parse_args()

if not os.path.exists(args.out):
  os.mkdir(args.out)

con = dh.read_json_file_raw(args.db, args.input)

Nv = list(dh.extract_set_all_values(con, 'matrix_dim'))
voi = 'time_op'
stat = 'mean'
machine = 'Poincare'
#machine = 'Ruche'
#ncore = 40
ncore = 16

for md in Nv:
  filter_prefix = f'pagerank_plots_d{md}'
  filter_dict = {'matrix_dim' : [md], 'test' : ['page_rank', 'personalized_page_rank'], 'C' : [300], 'success' : ['true'], 'machine' : [machine]}
  dh.create_filter(con, filter_prefix, filter_dict)
  dh.create_case_table(con, filter_prefix, ['test', 'lang', 'format', 'Q', 'cores', 'nodes', 'GR', 'GC'])
  dh.compute_stats(con, filter_prefix, voi)
  
  langv = list(dh.extract_set_all_values(con, 'lang'))
  testv = list(dh.extract_set_all_values(con, 'test'))
  Qv = list(dh.extract_set_all_values(con, 'Q'))
  formatv = list(dh.extract_set_all_values(con, 'format'))
  nodesv = list(dh.extract_set_all_values(con, 'nodes'))
  GRv = list(dh.extract_set_all_values(con, 'GR'))
  GCv = list(dh.extract_set_all_values(con, 'GC'))

  print(langv)
  print(Qv)

  m, coi_set = dr.matrix_relation(con, {'test' : [], 'lang' : [], 'format' : [], 'Q' : []}, ['GR', 'GC'], 'nodes', voi, filter_prefix, [stat])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_axis(m, coi_set, stat, 'Nodes (Cores)', 'Time', args.pv)
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, ncore)
  plot.save(fig, f'{args.out}/{machine}_d{md}.pdf')

  for l in langv:
    dict_cases = {'test' : [], 'lang' : [l], 'format' : [], 'Q' : []}
    list_sub_cases = ['GR', 'GC']
    m, coi_set = dr.matrix_relation(con, dict_cases, list_sub_cases, 'nodes', voi, filter_prefix, [stat])
    coi_set = sorted(coi_set, key=float)
    fig = plot.plot_axis(m, coi_set, stat, 'Nodes (Cores)', 'Time', args.pv)
    plot.plot_axis_add_cores_to_node_count(fig, coi_set, ncore)
    plot.save(fig, f'{args.out}/{machine}_d{md}_lang{l}.pdf')
    print(cmd.get_cmd(filter_dict, dict_cases, list_sub_cases, 'nodes', voi, args.input, f'{args.out}/{machine}_d{md}_lang{l}.pdf', 'Nodes (Cores)', 'Time', ncore))

  for l in langv:
    for f in formatv:
      m, coi_set = dr.matrix_relation(con, {'test' : [], 'lang' : [l], 'format' : [f], 'Q' : []}, [], 'nodes', voi, filter_prefix, [stat])
      coi_set = sorted(coi_set, key=float)
      fig = plot.plot_axis(m, coi_set, stat, 'Nodes (Cores)', 'Time', args.pv)
      plot.plot_axis_add_cores_to_node_count(fig, coi_set, ncore)
      plot.save(fig, f'{args.out}/{machine}_dimdist_d{md}_l{l}_f{f}.pdf')
      for q in Qv:
        m, coi_set = dr.matrix_relation(con, {'test' : [], 'lang' : [l], 'format' : [f], 'Q' : [q]}, [], 'nodes', voi, filter_prefix, [stat])
        coi_set = sorted(coi_set, key=float)
        fig = plot.plot_axis(m, coi_set, stat, 'Nodes (Cores)', 'Time', args.pv)
        plot.plot_axis_add_cores_to_node_count(fig, coi_set, ncore)
        plot.save(fig, f'{args.out}/{machine}_dimdist_d{md}_l{l}_f{f}_q{q}.pdf')
