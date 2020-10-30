import numpy as np

def table(m, filename):
  row_keys = set()
  column_keys = set()
  for v in m.values():
    for k , v in v.items():
      row_keys.add(k)
      for i in v.keys():
        if not i.startswith('__'):
          column_keys.add(i)
  row_keys = sorted(row_keys)
  column_keys = sorted(column_keys)

  r = ''
  r += '\\begin{tabular}{'
  r += 'c' * (len(column_keys) + 2)
  r += '}\n\\hline\n'

  r += 'Cases & Nodes'
  for i in column_keys:
    r += f'& {i}'
  r += '\\\\'
  r += '\n\\hline\n'

  for k in sorted(m.keys()):
    v = m[k]
    r += '\multirow{' + str(len(row_keys)) + '}{*}{' + str(k) + '}'
    for kr in row_keys:
      r += '& ' + str(kr)
      for kc in column_keys:
        r += '& ' + str(round(v[kr][kc], 4) if isinstance(v[kr][kc], float) else v[kr][kc])
      r += '\\\\\n'
    r += '\\hline\n'

  r += '\\end{tabular}\n'

  f = open(filename, 'w')
  f.write(r)
  f.close()
  return r
