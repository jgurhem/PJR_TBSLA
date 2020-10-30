
def get_cmd(filter_dict, cases_dict, sub_cases_list, coi, voi, input_file, output_file, xlabel = '', ylabel = '', cores_per_node = 0):
  s = 'python create_figure.py '
  s += f'{input_file} '
  for k, v in filter_dict.items():
    s += '-f ' + k + ':'
    for i in v:
      s += str(i) + ','
    s = s.rstrip(',')
    s += ' '
  for k, v in cases_dict.items():
    s += '-l ' + k + ':'
    for i in v:
      s += str(i) + ','
    s = s.rstrip(',')
    s = s.rstrip(':')
    s += ' '
  for i in sub_cases_list:
    s += '-s ' + i + ' '
  s += '-coi ' + coi
  s += ' -voi ' + voi
  s += ' -o ' + output_file
  if xlabel != '':
    s += ' -xlabel "' + xlabel + '"'
  if ylabel != '':
    s += ' -ylabel "' + ylabel + '"'
  if cores_per_node != 0:
    s += ' -cpn ' + str(cores_per_node)
  return s

