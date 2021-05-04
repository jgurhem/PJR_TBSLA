import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json
import re

def genlabel(in_):
  s = ''
  for i in in_:
    s += str(i) + ', '
  return s.rstrip(', ')

def FUNC_DEFAULT(x, y):
  return x

def plot_axis(m, coi_set, attribute, xlabel, ylabel, legend, pv, xscale = 'linear', yscale = 'linear', sort = True, func = FUNC_DEFAULT, keep_missing = True, nbest = 0):
  fig = plt.figure()
  ax = fig.gca()
  xvec = np.arange(len(coi_set))
  xdict = dict()
  ydict = dict()

  if sort:
    keys = sorted(m.keys(), key = lambda x:[int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)])
  else:
   keys = m.keys()
  for k in keys:
    v = m[k]
    if pv:
      print()
      print()
      print(k)
      for k2,v2 in v.items():
        print(k2, " :: ", v2)
    k_dict = json.loads(k)
    if keep_missing:
      x = xvec
      y = [func(v[x][attribute], v[x]) for x in coi_set]
    else:
      x = []
      y = []
      for i, j in zip(xvec, coi_set):
        val = func(v[j][attribute], v[j])
        if val != None:
          x.append(i)
          y.append(val)
    label = genlabel([k_dict[i] for i in legend])
    xdict[label] = x
    ydict[label] = y
  if nbest != 0 and keep_missing == True:
    bestordered = dict()
    toshow = set()
    for i in range(len(xvec)):
      bestordered[i] = sorted(ydict.keys(), key = lambda x:ydict[x][i])
      if nbest > 0:
        toshow.update(list(bestordered[i][:nbest]))
      else:
        toshow.update(list(bestordered[i][nbest:]))
    toshow = sorted(toshow)
    for k in toshow:
      ax.plot(xdict[k], ydict[k], label = k, marker='*')
  else:
    for k in xdict.keys():
      ax.plot(xdict[k], ydict[k], label = k, marker='*')

  ax.set_ylabel(ylabel)
  ax.set_xlabel(xlabel)
  ax.set_xscale(xscale)
  ax.set_yscale(yscale)
  if yscale == 'log':
    #ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(1.00))
    #ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.25))
    ax.yaxis.set_major_locator(mpl.ticker.LogLocator(subs='all', base=5))
    ax.yaxis.set_minor_locator(mpl.ticker.LogLocator(subs='all', base=5))
    ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mpl.ticker.ScalarFormatter())
  ax.xaxis.set_ticks(xvec)
  ax.xaxis.set_ticklabels(coi_set)
  #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0))
  #ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1))
  ax.legend(loc='best')
  return fig

def plot_bar(m, coi_set, attribute, xlabel, ylabel, legend, pv, xscale = 'linear', yscale = 'linear'):
  fig = plt.figure()
  ax = fig.gca()
  xvec = np.arange(len(coi_set))
  width = 0.85
  len_mkeys = len(m.keys())
  pos = 0

  for k in sorted(m.keys(), key = lambda x:[int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)]):
    v = m[k]
    if pv:
      print()
      print()
      print(k)
      for k2,v2 in v.items():
        print(k2, " :: ", v2)
    k_dict = json.loads(k)
    xvec_bar = []
    for i in xvec:
      xvec_bar.append(i + pos * width / len_mkeys - width / 2 + width / len_mkeys / 2)
    rects = ax.bar(xvec_bar, [v[x][attribute] for x in coi_set], width / len_mkeys, label=genlabel([k_dict[i] for i in legend]))
    for rect in rects:
      height = rect.get_height()
      ax.annotate(f'{height:.0f}', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(1, 3), textcoords="offset pixels", rotation=90, size=9, in_layout=True, ha='center', va='bottom')
    pos = pos + 1

  ax.set_ylabel(ylabel)
  ax.set_xlabel(xlabel)
  ax.set_xscale(xscale)
  ax.set_yscale(yscale)
  if yscale == 'log':
    ax.yaxis.set_major_locator(mpl.ticker.LogLocator(subs='all', base=5))
    ax.yaxis.set_minor_locator(mpl.ticker.LogLocator(subs='all', base=5))
    ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mpl.ticker.ScalarFormatter())
  ax.xaxis.set_ticks(xvec)
  ax.xaxis.set_ticklabels(coi_set)
  plt.margins(y=0.12)
  ax.legend(loc='best')
  return fig

def plot_ratios_1_on_n_axis(m, coi_set, attribute, xlabel, ylabel, legend, pv, xscale = 'linear', yscale = 'linear', ideal = True):
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
    yvec = []
    for x in coi_set:
      if v[x][attribute] == None:
        yvec.append(None)
      else:
        yvec.append(v[coi_set[0]][attribute] / v[x][attribute])
    ax.plot(xvec, yvec, label=genlabel([k_dict[i] for i in legend]), marker='*')

  if ideal:
    ideald = dict()
    pos = 1
    for i in sorted(coi_set, key=float):
      ideald[i] = pos
      pos *= 2
    ax.plot(ideald.keys(), ideald.values(), label='Ideal')

  ax.set_ylabel(ylabel)
  ax.set_xlabel(xlabel)
  ax.set_xscale(xscale)
  ax.set_yscale(yscale)
  if yscale == 'log':
    ax.yaxis.set_major_locator(mpl.ticker.LogLocator(subs='all', base=2))
    ax.yaxis.set_minor_locator(mpl.ticker.LogLocator(subs='all', base=2))
    ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mpl.ticker.ScalarFormatter())
  ax.xaxis.set_ticks(xvec)
  ax.xaxis.set_ticklabels(coi_set)
  ax.legend(loc='best')
  return fig

def plot_ratios_n_on_1_axis(m, coi_set, attribute, xlabel, ylabel, legend, pv, xscale = 'linear', yscale = 'linear', ideal = True):
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
    yvec = []
    for x in coi_set:
      if v[x][attribute] == None:
        yvec.append(None)
      else:
        yvec.append(v[x][attribute] / v[coi_set[0]][attribute])
    ax.plot(xvec, yvec, label=genlabel([k_dict[i] for i in legend]), marker='*')

  if ideal:
    ideald = dict()
    pos = 1
    for i in sorted(coi_set, key=float):
      ideald[i] = pos
      pos *= 2
    ax.plot(ideald.keys(), ideald.values(), label='Ideal')

  ax.set_ylabel(ylabel)
  ax.set_xlabel(xlabel)
  ax.set_xscale(xscale)
  ax.set_yscale(yscale)
  if yscale == 'log':
    ax.yaxis.set_major_locator(mpl.ticker.LogLocator(subs='all', base=2))
    ax.yaxis.set_minor_locator(mpl.ticker.LogLocator(subs='all', base=2))
    ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(mpl.ticker.ScalarFormatter())
  ax.xaxis.set_ticks(xvec)
  ax.xaxis.set_ticklabels(coi_set)
  ax.legend(loc='best')
  return fig

def save(fig, out_file):
  fig.savefig(out_file, bbox_inches="tight", metadata={'CreationDate': None})
  plt.close()

def rotate_xticks(xticklabels):
  plt.xticks(rotation='90')
  plt.margins(x = 0.01)
  plt.gcf().canvas.draw()
  tl = plt.gca().get_xticklabels()
  if len(tl) == 0: return
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
    xlab.append(str(i) + ' (' + str(int(i) * cores_per_nodes) + ')')
  ax.xaxis.set_ticklabels(xlab)
  return fig

def grid(fig, axis):
  #plt.grid(axis=axis, linestyle=':', linewidth='0.5', color='black')
  plt.grid(axis=axis, linestyle=':', color='black')
  return fig
