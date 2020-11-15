import numpy as np
import json
import re

def table(m, filename, legend):
  row_keys = set()
  column_keys = set()
  N_key = ''
  for v in m.values():
    for k , v in v.items():
      row_keys.add(k)
      for i in v.keys():
        if not i.startswith('__'):
          column_keys.add(i)
        if i.startswith('__') and i.endswith('.N'):
          N_key = i
  row_keys = sorted(row_keys)
  column_keys = sorted(column_keys)

  r = ''
  r += '\\begin{tabular}{'
  r += 'c' * (len(column_keys) + 2)
  r += '}\n\\hline\n'

  r += 'Cases & Nodes'
  for i in column_keys:
    r += f'& {i}'
  r += ' & N \\\\'
  r += '\n\\hline\n'

  for k in sorted(m.keys(), key = lambda x:[int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)]):
    v = m[k]
    k_dict = json.loads(k)
    r += '\multirow{' + str(len(row_keys)) + '}{*}{' + str(tuple([k_dict[i] for i in legend])) + '}'
    for kr in row_keys:
      r += '& ' + str(kr)
      for kc in column_keys:
        r += '& ' + str(round(v[kr][kc], 4) if isinstance(v[kr][kc], float) else v[kr][kc])
      r += '& ' + str(v[kr].get(N_key, 0))
      r += '\\\\\n'
    r += '\\hline\n'

  r += '\\end{tabular}\n'

  f = open(filename, 'w')
  f.write(r)
  f.close()
  return r
