import sqlite3
import warnings
warnings.filterwarnings('ignore', message='Unknown infodict keyword:.*')
from ..pjr import DBRelator as dr
from . import mpl as plot
from . import latex as table
import matplotlib as mpl
import matplotlib.pyplot as plt
import json


def get_nnz(y):
  nnz = 0
  if y['matrixtype'] == 'cqmat':
    nnz = y['NR'] * y['C'] - y['C'] * (y['C'] - 1) / 2
  elif y['matrixtype'] == 'nlpkkt120':
    nnz = 96845792
  elif y['matrixtype'] == 'nlpkkt200':
    nnz = 448225632
  elif y['matrixtype'] == 'cage14':
    nnz = 27130349
  elif y['matrixtype'] == 'cage15':
    nnz = 99199551
  return nnz

def gflops(x, y):
  if x == None: return None
  nnz = get_nnz(y)
  f = 0
  if y['op'] == 'a_axpx' or y['op'] == 'AAxpAx':
    f = (4 * nnz - y['NC'])
  elif y['op'] == 'AAxpAxpx':
    f = 4 * nnz
  elif y['op'] == 'spmv' or y['op'] == 'spmv_no_redist' or y['op'] == 'Ax' or y['op'] == 'Ax_':
    f = (2 * nnz - y['NC'])
  elif y['op'] == 'pagerank':
    f = (2 * nnz + 3 * int(y['matrix_dim'])) * int(y['nb_iterations']) + 2 * int(y['matrix_dim'])
  return f / x / 1e9

class Flops:
  def __init__(self, path):
    self.f = gflops
    self.n = 'GFlops'
    self.p = path + '/flops/'
    self.s = -1

class Identity:
  def __init__(self, path):
    self.f = plot.FUNC_DEFAULT
    self.n = 'Time (s)'
    self.p = path + '/time/'
    self.s = 1

def dict_to_name(d):
  s = ''
  for k, v in d.items():
    s += f'_{k}['
    for i in v:
      s += f'{i}+'
    s = s.rstrip('+')
    s += ']'
  return s

def dict_to_metakey(d):
  s = ''
  for k, v in d.items():
    s += f'-{k}{v}'
  s = s.lstrip('-')
  return s

def get_info_case(con, casedef, caseid):
  cur = con.cursor()
  query = 'SELECT '
  for i in casedef:
    query += f'auto_cases.{i},'
  query = query.rstrip(',')
  query += f' FROM auto_cases where rowid = {caseid}'
  cur.execute(query)
  r = cur.fetchone()
  return r


class PlotGenerator:
  def __init__(self, output_db, stat, coi, xlabel, voi, npcn, casedefsub, rcparams):
    self.output_db = output_db
    self.coi = coi
    self.xlabel = xlabel
    self.voi = voi
    self.npcn = npcn
    self.stat = stat
    self.casedefsub = casedefsub
    self.rcparams = rcparams
    self.xscale = 'linear'
    self.yscale = 'linear'
    self.enable_auto_title = True
    self.add_metadata = True

  def set_xscale(self, xscale):
    self.xscale = xscale

  def set_yscale(self, yscale):
    self.yscale = yscale

  def set_enable_auto_title(self, enable_auto_title):
    self.enable_auto_title = enable_auto_title

  def set_add_metadata(self, add_metadata):
    self.add_metadata = add_metadata

  def pdf(self, path, filter_dict, list_cases, list_sub_cases, columns, ylabel, func, nbest = 0, suffix = "", ratios = list()):
    mpl.rcParams.update(self.rcparams)
    con = sqlite3.connect(self.output_db)
    m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, self.coi, self.voi, 'auto', [self.stat], ratios = ratios)
    if len(m) > 0:
      coi_set = sorted(coi_set, key=float)
      fig = plot.plot_axis(m, coi_set, self.stat, self.xlabel, ylabel, list_cases, False, func = func, nbest = nbest, xscale = self.xscale, yscale = self.yscale)
      if self.npcn > 1:
        plot.plot_axis_add_cores_to_node_count(fig, coi_set, self.npcn)
      output_file_base = path + 'fig' + dict_to_name(filter_dict) + suffix
      bbox_inches = 'tight'
      if self.enable_auto_title:
        bbox_inches = None
        plt.title(dict_to_name(filter_dict).lstrip('_').replace(']_','] _'), wrap = True)
      metadata = dict()
      if self.add_metadata:
        cmd = ''
        for k1, d1 in m.items():
          for k2, d2 in d1.items():
            k1d = json.loads(k1)
            k1d[self.coi] = k2
            caseid = d2['__auto_cases.rowid']
            if caseid != None:
              metadata[dict_to_metakey(k1d) + '-sqlcasequery'] = d2['__sql_case_query']
              metadata[dict_to_metakey(k1d) + '-sqlcontrib'] = d2['__sql_get_contributions']
              infocase = get_info_case(con, self.casedefsub, caseid)
              cmd += 'python tools/submit.py'
              for c, i in zip(self.casedefsub, infocase):
                if i != None:
                  cmd += f' --{c} {i}'
              cmd += ';'
        metadata['submitcmd'] = cmd
      plot.save(fig, output_file_base + '.pdf', bbox_inches = bbox_inches, metadata = metadata)
      table.table(m, output_file_base + '.tex', list_cases, self.stat, columns, func = func)
      print(output_file_base + '.pdf')
    con.close()
