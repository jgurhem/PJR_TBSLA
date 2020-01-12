import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def plot_axis(m, coi_set, attribute, xlabel, ylabel, pv):
  fig = plt.figure()
  ax = fig.gca()
  xvec = np.arange(len(coi_set))

  for k in sorted(m.keys()):
    v = m[k]
    if pv:
      print(k, {k2:round(v2, 4) if isinstance(v2, float) else v2 for k2,v2 in v.items()})
    ax.plot(xvec, [v[str(x) + '_' + attribute] for x in coi_set], label=str(k).replace("'",''), marker='*')

  ax.set_ylabel(ylabel)
  ax.set_xlabel(xlabel)
  ax.xaxis.set_ticklabels(coi_set)
  ax.xaxis.set_ticks(xvec)
  ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  return fig

def save(fig, out_file):
  fig.savefig(out_file, bbox_inches="tight")
  plt.close()
