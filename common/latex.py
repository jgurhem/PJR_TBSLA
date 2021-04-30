import numpy as np
import json
import re

def table(m, filename, legend, columns = list()):
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

  for k in sorted(m.keys(), key = lambda x:[int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)]):
    v = m[k]
    k_dict = json.loads(k)
    r += '\multirow{' + str(len(row_keys)) + '}{*}{' + str(tuple([k_dict[i] for i in legend])) + '}'
    for kr in row_keys:
      r += '& ' + str(kr)
      for kc in column_keys:
        r += '& ' + str(round(v[kr][kc], 4) if isinstance(v[kr][kc], float) else v[kr][kc])
      r += '& ' + str(v[kr].get(Nval_key, 0))
      r += '& ' + str(v[kr].get(Ncase_key, 0))
      r += '\\\\\n'
    r += '\\hline\n'

  r += '\\end{tabular}\n'

  f = open(filename, 'w')
  f.write(r)
  f.close()
  return r
