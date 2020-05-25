import pjr.DBAggregator as da
from bs4 import BeautifulSoup

def compute_dist(casediff, prefix1, prefix2):
  for case, data in casediff.items():
    if case == '__case_names': continue
    if prefix1 in data and prefix2 in data:
      data['_diff'] = dict()
      for i in da.CASES_DATA:
        #data['_diff'][i] = (data[prefix1][i] - data[prefix2][i]) / data[prefix1][i]
        data['_diff'][i] = data[prefix1][i] / data[prefix2][i]

def _gen_prefix_html(data, prefix, val):
  s = '<td>'
  if prefix in data:
    v = data[prefix][val]
    if isinstance(v, float):
      s += f'{v:.5f}'
    else:
      s += f'{v}'
  s += '</td>'
  return s
  

def print_diff_html(casediff, prefix1, prefix2):
  s = ''
  s += '<script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.js"></script>'
  s += '<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.js"></script>'
  s += '<script src="https://unpkg.com/floatthead"></script>'
  s += '<style>'
  s += '<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.css">'
  s += '.data_table_div {}'
  s += '.data_table_div table {width:100%; font-size:14:px;}'
  s += '.data_table_div table th, tr, td {border:1px solid #cecfd5; text-align:center;}'
  s += '.data_table_div table th {background-color:#cecfd5; height:30px;}'
  s += '.data_table_div table tr td.pickHeading {}'
  s += '</style> \n'
  s += '<script>\n'
  s += '$(document).ready( function () { $("#data_table_id").DataTable({"paging": false});} );'
  s += '$(() => $("table").floatThead());'
  s += '</script>\n'

  s += '<div class="data_table_div">'
  s += '<table class="data_table_class" id="data_table_id" cellpadding="1" cellspacing="0">\n'
  s += '<thead>\n'
  s += '<tr>'
  for i in casediff['__case_names']:
    s += f'<th>{i[0]}</th>'
  s += f'<th colspan="2">n</th>'
  s += f'<th colspan="3">mean</th>'
  s += '</tr>\n'
  s += '<tr>'
  case_names_len = len(casediff['__case_names'])
  s += f'<th colspan="{case_names_len}"></th>'
  s += f'<th>old</th>'
  s += f'<th>new</th>'
  s += f'<th>old</th>'
  s += f'<th>new</th>'
  s += f'<th>old/new</th>'
  s += '</tr>\n'
  s += '</thead>\n'

  for case, data in casediff.items():
    if case == '__case_names': continue
    s += '<tr>'
    for i in case:
      s += f'<td>{i}</td>'
    s += _gen_prefix_html(data, prefix1, 'n')
    s += _gen_prefix_html(data, prefix2, 'n')
    s += _gen_prefix_html(data, prefix1, 'mean')
    s += _gen_prefix_html(data, prefix2, 'mean')
    s += _gen_prefix_html(data, '_diff', 'mean')
    s += '</tr>\n'

  s += '</table></div>'
  #s = BeautifulSoup(s, 'html.parser').prettify()
  print(s)
  return s
