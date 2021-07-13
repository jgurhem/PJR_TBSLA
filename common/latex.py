import numpy as np
import json
import re
from .mpl import genlabel, FUNC_DEFAULT
from ..pjr import DBHelper as dh
import sqlite3

def sort_func(x):
  return re.split(r'([^0-9.]+)', x)

def table(m, filename, legend, stat, columns = list(), func = FUNC_DEFAULT):
  row_keys = set()
  column_keys = set()
  Nval_key = ''
  Ncase_key = ''
  for v in m.values():
    for k , v in v.items():
      row_keys.add(k)
      for i in v.keys():
        if not i.startswith('__') and (len(columns) == 0 or (len(columns) > 0 and i in columns)):
          column_keys.add(i)
        if i.startswith('__') and i.endswith('.Nval'):
          Nval_key = i
        if i.startswith('__') and i.endswith('.Ncase'):
          Ncase_key = i
  row_keys = sorted(row_keys)
  column_keys = sorted(column_keys)

  r = ''
  r += '\\begin{tabular}{'
  r += 'c' * (len(column_keys) + 4)
  r += '}\n\\hline\n'

  r += 'Cases & Nodes'
  for i in column_keys:
    newi = str(i).replace("_", "\_")
    r += f'& {newi}'
  r += ' & N & Ncase \\\\'
  r += '\n\\hline\n'

  for k in sorted(m.keys(), key = sort_func):
    v = m[k]
    k_dict = json.loads(k)
    r += '\multirow{' + str(len(row_keys)) + '}{*}{' + genlabel([k_dict[i] for i in legend]) + '}'
    for kr in row_keys:
      r += '& ' + str(kr)
      for kc in column_keys:
        if kc == stat:
          val = func(v[kr][kc], v[kr])
        else:
          val = v[kr][kc]
        r += '& ' + str(round(val, 4) if isinstance(val, float) else val)
      r += '& ' + str(v[kr].get(Nval_key, 0))
      r += '& ' + str(v[kr].get(Ncase_key, 0))
      r += '\\\\\n'
    r += '\\hline\n'

  r += '\\end{tabular}\n'

  f = open(filename, 'w')
  f.write(r)
  f.close()
  return r


def table2(db, relname, filter_dict, cases, sub_cases, sub_col, stat, coi, voi, func = FUNC_DEFAULT, dec = 2):
  con = sqlite3.connect(db)
  cur = con.cursor()
  s = ''

  query = f'SELECT DISTINCT {coi} FROM {relname}_cases WHERE'
  query += dh.generate_conditions_where(filter_dict)
  if query.endswith(' WHERE'):
    query = query[:-6]
  cur.execute(query)
  res = cur.fetchall()
  columns = [x[0] for x in res]
  columns = sorted(columns)

  query = f'SELECT DISTINCT {sub_col} FROM {relname}_cases WHERE'
  query += dh.generate_conditions_where(filter_dict)
  if query.endswith(' WHERE'):
    query = query[:-6]
  cur.execute(query)
  res = cur.fetchall()
  scolumns = [x[0] for x in res]
  scolumns = sorted(scolumns)

  query = 'SELECT DISTINCT '
  for i in cases:
    query += i + ','
  query = query.rstrip(',')
  query += f' FROM {relname}_cases WHERE'
  query += dh.generate_conditions_where(filter_dict)
  if query.endswith(' WHERE'):
    query = query[:-6]
  cur.execute(query)
  rows = cur.fetchall()
  rows = sorted(rows, key = sort_func):


  s += '\\begin{tabular}{'
  s += 'c' * (len(cases) + len(scolumns) * len(columns))
  s += '}\n\\hline\n'

  for i in cases:
    s += '\multirow{2}{*}{' + str(i).replace('_', '\_') + '} &'
  for sc in scolumns:
    s += ' \multicolumn{' + str(len(columns)) + '}{c}{' + str(sc).replace('_', '\_') + '} &'
  s = s.rstrip('&')
  s+= '\\\\\n'
  for i in range(len(cases) - 1):
    s += '&'
  for sc in scolumns:
    for c in columns:
      s += f'& {c}'
  s+= '\\\\\n'
  s += '\\hline\n'

  for r in rows:
    for i in r:
      if i != None:
        s += f' {i}'
      s += ' &'
    s = s.rstrip('&')
    for sc in scolumns:
      for c in columns:
        keys = [stat] + sub_cases + ['rowid', 'N']
        query = f'SELECT {relname}_{voi}_stats.{stat}'
        for i in sub_cases:
          query += f',{relname}_cases.{i}'
        query += f',{relname}_cases.rowid,{relname}_{voi}_stats.N FROM {relname}_{voi}_stats INNER JOIN {relname}_cases ON {relname}_{voi}_stats.rowid={relname}_cases.rowid WHERE '
        query += f"{coi}='{c}'"
        query += f"AND {sub_col}='{sc}'"
        for i in range(len(cases)):
          if r[i] == None:
            query += f' AND {relname}_cases.' + cases[i] + " is null"
          else:
            query += f' AND {relname}_cases.' + cases[i] + "='" + str(r[i]) + "'"
        query += ' AND '
        query += dh.generate_conditions_where(filter_dict, f'{relname}_cases')
        if query.endswith(' AND '):
          query = query[:-5]
        cur.execute(query)
        res = cur.fetchall()
        if res != None and len(res) > 0:
          min_pos = np.argmin([float(x[0]) for x in res])
          v = res[min_pos][0]
          d = dict(zip(keys, res[min_pos]))
          s += f' & {func(v, d):.{dec}f}'
    s += ' \\\\\n'
  s += '\\hline\n'
  s += '\\end{tabular}\n'

  return s
