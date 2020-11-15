import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json
import re

def plot_axis(m, coi_set, attribute, xlabel, ylabel, legend, pv):
  fig = plt.figure()
  ax = fig.gca()
  xvec = np.arange(len(coi_set))

  for k in sorted(m.keys(), key = lambda x:[int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)]):
    v = m[k]
    if pv:
      print()
      print()
      print(k)
      for k2,v2 in v.items():
        print(k2, " :: ", v2)
    k_dict = json.loads(k)
    ax.plot(xvec, [v[x][attribute] for x in coi_set], label=str(tuple([k_dict[i] for i in legend])).replace("'",''), marker='*')

  ax.set_ylabel(ylabel)
  ax.set_xlabel(xlabel)
  ax.xaxis.set_ticks(xvec)
  ax.xaxis.set_ticklabels(coi_set)
  ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  return fig

def save(fig, out_file):
  fig.savefig(out_file, bbox_inches="tight", metadata={'CreationDate': None})
  plt.close()

def rotate_xticks(xticklabels):
  plt.xticks(rotation='90')
  plt.margins(x = 0.01)
  plt.gcf().canvas.draw()
  tl = plt.gca().get_xticklabels()
  maxsize = max([t.get_window_extent().width for t in tl])
  m = 0.3 # inch margin
  s = maxsize / plt.gcf().dpi * len(xticklabels) + 2 * m
  margin = m / plt.gcf().get_size_inches()[0]
  plt.gcf().subplots_adjust(left=margin, right=1. - margin)
  plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

def plot_axis_add_cores_to_node_count(fig, node_set, cores_per_nodes):
  ax = fig.gca()
  xlab = list()
  for i in node_set:
    xlab.append(str(i) + ' (' + str(i * cores_per_nodes) + ')')
  ax.xaxis.set_ticklabels(xlab)
  return fig

def grid(fig, axis):
  #plt.grid(axis=axis, linestyle=':', linewidth='0.5', color='black')
  plt.grid(axis=axis, linestyle=':', color='black')
  return fig
