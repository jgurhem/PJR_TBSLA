import common.data as cd
import pickle

casediff = pickle.load(open('.agg_data.pkl', 'rb'))
cd.compute_dist(casediff, 'db1', 'db2')
cd.print_diff_html(casediff, 'db1', 'db2')
