import pjr.DBHelper as dh
import pjr.DBRelator as dr
import argparse
import common.parser as cp
import common.properties as prop
import common.mpl as plot
import itertools

def get_values(con, rowid, case_def, relname):
  query = "SELECT "
  for i in case_def:
    query += f"{i},"
  query = query.rstrip(',')
  query += f" FROM {relname}_cases WHERE rowid={rowid}"
  cur = con.cursor()
  cur.execute(query)
  res = cur.fetchone()
  return res

def job_already_done(con, case_def, relname, v):
  query = "SELECT "
  for i in case_def:
    query += f"{i},"
  query = query.rstrip(',')
  query += f" FROM {relname}_cases WHERE"
  for i in range(len(case_def)):
    query += f' {relname}_cases.' + case_def[i] + "='" + str(v[i]) + "' AND"
  if query.endswith(' AND'):
    query = query[:-4]
  cur = con.cursor()
  cur.execute(query)
  res = cur.fetchone()
  return res != None

def gen_values(case_def, in_, nodes, cores, v):
  gr = in_[0]
  gc = in_[1]
  r = []
  for i in case_def:
    if i == 'CPT':
      r.append(None)
    elif i == 'GR':
      r.append(gr)
    elif i == 'GC':
      r.append(gc)
    elif i == 'LGR':
      r.append(None)
    elif i == 'LGC':
      r.append(None)
    elif i == 'BGR':
      r.append(None)
    elif i == 'BGC':
      r.append(None)
    else:
      r.append(__get(v, case_def, i))
  return tuple(r)

def gen_values_yml(case_def, in_, nodes, cores, v):
  cpt = in_[1]
  bgr = in_[2]
  bgc = in_[3]
  gr = in_[0][0]
  gc = in_[0][1]
  lgr = int(gr / bgr)
  lgc = int(gc / bgc)
  if lgc == 0 or lgr == 0 or lgc * lgr != cpt or gr != bgr * lgr or gc != bgc * lgc or cpt > nodes * cores: return None
  r = []
  for i in case_def:
    if i == 'CPT':
      r.append(cpt)
    elif i == 'GR':
      r.append(gr)
    elif i == 'GC':
      r.append(gc)
    elif i == 'LGR':
      r.append(lgr)
    elif i == 'LGC':
      r.append(lgc)
    elif i == 'BGR':
      r.append(bgr)
    elif i == 'BGC':
      r.append(bgc)
    else:
      r.append(__get(v, case_def, i))
  return tuple(r)

def __get(v, case_def, param):
  r = v[case_def.index(param)]
  if r == None:
    return 0
  return r

def gen_cmd(case_def, values):
  cmd = "python tools/submit.py --matrix-type cqmat --timeout 60 --wall-time 4"
  if __get(values, case_def, 'lang') == "YML":
    cmd += " --compile"
  for i in range(len(case_def)):
    if values[i] != None:
      cmd += f" --{case_def[i]} {values[i]}"
  return cmd

def __diff(v1, v2, case_def, param1, param2):
  d = ((__get(v1, case_def, param1) - __get(v2, case_def, param2)) / (__get(v1, case_def, param1) + __get(v2, case_def, param2) + 1)) ** 2
  d += ((__get(v2, case_def, param1) - __get(v1, case_def, param2)) / (__get(v2, case_def, param1) + __get(v1, case_def, param2) + 1)) ** 2
  if d == 0:
    d = float(1.0 / (__get(v1, case_def, param1) * __get(v2, case_def, param2) * __get(v2, case_def, param1) * __get(v1, case_def, param2) + 1))
  return d

def score(v1, v2, case_def):
  s = 0
  s += __diff(v1, v2, case_def, 'GR', 'GC')
  s += __diff(v1, v2, case_def, 'BGR', 'BGC')
  s += __diff(v1, v2, case_def, 'LGR', 'LGC')
  s += (__get(v1, case_def, 'CPT') - __get(v2, case_def, 'CPT')) / (__get(v1, case_def, 'CPT') + __get(v2, case_def, 'CPT') + 1)
  s += (__get(v1, case_def, 'C') - __get(v2, case_def, 'C')) / (__get(v1, case_def, 'C') + __get(v2, case_def, 'C'))
  return s

def decomp(n):
  i = 2
  factors = []
  while i * i <= n:
    if n % i:
      i += 1
    else:
      n //= i
      factors.append(i)
  if n > 1:
    factors.append(n)
  return factors

def decomp_pairs(n):
  pairs = []
  d = 1
  factors = decomp(n)
  for i in factors:
    d = d * i
    pairs.append((n // d, d))
    pairs.append((d, n // d))
  return sorted(set(pairs))

parser = argparse.ArgumentParser(parents=[cp.get_common()])
parser.add_argument('-voi', type=str, help='value of interest', dest='voi', required=True)
parser.add_argument('-op', type=str, help='Operation used to compute statistics on the values of the same case (mean, min, max, median, sum, std, var)', dest='op', default='mean')
parser.add_argument('-dbo', type=str, help='Name of the output database file', dest='dbo', default='test.db')
parser.add_argument('-n', type=int, help='Number of tests to show', dest='ntest', default=3)
parser.add_argument('-ncores', type=int, help='Number of cores to consider', dest='ncores', required=True)
parser.add_argument('-show-done', help='Show generated command to reproduce tests already performed', dest='showdone', default=False, action='store_true')
parser.add_argument('-show-new', help='Show generated command to make new tests', dest='shownew', default=False, action='store_true')
parser.add_argument('-show-best', help='Show command to reproduce best tests performed', dest='showbest', default=False, action='store_true')
args = parser.parse_args()

filter_dict = dh.convert_filter_list_to_dic(args.filter_list)

SUBMISSION_CASES = ['op', 'lang', 'format', 'nodes', 'machine', 'GR', 'GC', 'NR', 'NC', 'LGR', 'LGC', 'BGR', 'BGC', 'CPT', 'C']
GENERAL_CASES = ['nodes', 'lang', 'format']
CPT = [args.ncores, 2 * args.ncores, 3 * args.ncores, 4 * args.ncores]
BLOCKS = [1, 2, 4, 6, 8, 12, 16]

input_res = dh.read_json_file(args.dbo, args.input, filter_dict, SUBMISSION_CASES, [args.voi])
res = dr.best_cases_relation(input_res, GENERAL_CASES, args.voi, 'auto', [args.op], args.ntest)

max_size = 0
for k,v in res.items():
  s = len(str(k))
  if s > max_size:
    max_size = s

for k,v in res.items():
  print()
  print(f'#{str(k):{max_size + 1}s}', v)
  best_v = get_values(input_res, v[0], SUBMISSION_CASES, 'auto')
  for i in v:
    gv = get_values(input_res, i, SUBMISSION_CASES, 'auto')
    cmd = gen_cmd(SUBMISSION_CASES, gv)
    if args.showbest:
      print(cmd)
    s = score(best_v, gv, SUBMISSION_CASES)

  nodes = __get(k, GENERAL_CASES, 'nodes')
  factors = decomp_pairs(nodes * args.ncores)
  vs_list = []
  if __get(k, GENERAL_CASES, 'lang') == 'YML':
    GENERATED_CASES = list(itertools.product(factors, CPT, BLOCKS, BLOCKS))
    for in_ in GENERATED_CASES:
      gv = gen_values_yml(SUBMISSION_CASES, in_, nodes, args.ncores, best_v)
      if gv != None:
        s = score(best_v, gv, SUBMISSION_CASES)
        jad = job_already_done(input_res, SUBMISSION_CASES, 'auto', gv)
        vs_list.append((s, jad, gv))

  elif __get(k, GENERAL_CASES, 'lang') == 'MPI' or __get(k, GENERAL_CASES, 'lang') == 'HPX':
    for in_ in factors:
      gv = gen_values(SUBMISSION_CASES, in_, nodes, args.ncores, best_v)
      if gv != None:
        s = score(best_v, gv, SUBMISSION_CASES)
        jad = job_already_done(input_res, SUBMISSION_CASES, 'auto', gv)
        vs_list.append((s, jad, gv))

  vs_list = sorted(vs_list, key = lambda x : x[0])
  for vs in vs_list[:args.ntest]:
    if (args.shownew and not vs[1]) or (args.showdone and vs[1]):
      print(gen_cmd(SUBMISSION_CASES, vs[2]))

