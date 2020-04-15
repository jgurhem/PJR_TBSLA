import pjr.DBHelper as dh
import pjr.DBRelator as dr
import argparse
import common.properties as prop
import common.mpl as plot
import os

parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file')
parser.add_argument('-par', help='Print attributes range', dest='par', default=False, action='store_true')
parser.add_argument('-pv', help='Print values for the figure', dest='pv', default=False, action='store_true')
parser.add_argument('-db', help='Database file path', dest='db', default='tbsla/all_plot.db')
parser.add_argument('-o', help='Output directory path', dest='out', default='tbsla/all_plot')
args = parser.parse_args()

if not os.path.exists(args.out):
  os.mkdir(args.out)

con = dh.read_json_file_raw(args.db, args.input)

NCv = list(dh.extract_set_all_values(con, 'NC'))
voi = 'time_op'
stat = 'mean'

for nc in NCv:
  filter_prefix = f'all_plots_nc{nc}'
  dh.create_filter(con, filter_prefix, {'NC' : [nc], 'test' : ['a_axpx'], 'C' : [300], 'matrixtype' : ['cqmat'], 'success' : ['true'], 'machine' : ['Poincare']})
  dh.create_case_table(con, filter_prefix, ['lang', 'format', 'Q', 'nodes', 'GR', 'GC'])
  dh.compute_stats(con, filter_prefix, voi)
  
  langv = list(dh.extract_set_all_values(con, 'lang'))
  Qv = list(dh.extract_set_all_values(con, 'Q'))
  formatv = list(dh.extract_set_all_values(con, 'format'))

  print(langv)
  print(Qv)

  for q in Qv:
    m, coi_set = dr.matrix_relation(con, {'lang' : [], 'format' : [], 'Q' : [q]}, ['GR', 'GC'], 'nodes', voi, filter_prefix, [stat])
    coi_set = sorted(coi_set, key=float)
    fig = plot.plot_axis(m, coi_set, stat, 'nodes', 'Time', args.pv)
    plot.save(fig, f'{args.out}/nc{nc}_q{q}.pdf')

    for l in langv:
      m, coi_set = dr.matrix_relation(con, {'lang' : [l], 'format' : [], 'Q' : [q]}, ['GR', 'GC'], 'nodes', voi, filter_prefix, [stat])
      coi_set = sorted(coi_set, key=float)
      fig = plot.plot_axis(m, coi_set, stat, 'nodes', 'Time', args.pv)
      plot.save(fig, f'{args.out}/nc{nc}_q{q}_lang{l}.pdf')

  for f in formatv:
    m, coi_set = dr.matrix_relation(con, {'lang' : [], 'format' : [f], 'Q' : []}, ['GR', 'GC'], 'nodes', voi, filter_prefix, [stat])
    coi_set = sorted(coi_set, key=float)
    fig = plot.plot_axis(m, coi_set, stat, 'nodes', 'Time', args.pv)
    plot.save(fig, f'{args.out}/nc{nc}_format{f}.pdf')

    for l in langv:
      m, coi_set = dr.matrix_relation(con, {'lang' : [l], 'format' : [f], 'Q' : []}, ['GR', 'GC'], 'nodes', voi, filter_prefix, [stat])
      coi_set = sorted(coi_set, key=float)
      fig = plot.plot_axis(m, coi_set, stat, 'nodes', 'Time', args.pv)
      plot.save(fig, f'{args.out}/nc{nc}_format{f}_lang{l}.pdf')
  
  m, coi_set = dr.matrix_relation(con, {'lang' : [], 'format' : [], 'Q' : [0.2, 0.4, 0.6]}, ['GR', 'GC'], 'nodes', voi, filter_prefix, [stat])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_axis(m, coi_set, stat, 'nodes', 'Time', args.pv)
  plot.save(fig, f'{args.out}/nc{nc}_nodes.pdf')

  m, coi_set = dr.matrix_relation(con, {'lang' : [], 'format' : [], 'nodes' : []}, ['GR', 'GC'], 'Q', voi, filter_prefix, [stat])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_axis(m, coi_set, stat, 'Q', 'Time', args.pv)
  plot.save(fig, f'{args.out}/nc{nc}_q.pdf')
