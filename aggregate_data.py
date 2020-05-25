import pjr.DBHelper as dh
import pjr.DBAggregator as da
import argparse
import common.parser as cp
import common.properties as prop
import pickle

parser = argparse.ArgumentParser(parents=[cp.get_common()])
parser.add_argument('-l', '--list-cases', type=str, help='list of attributes to compare against the case of interest', action='append', dest='list_cases', required=True)
parser.add_argument('-dbo', type=str, help='Name of the output database file', dest='dbo', default='test.db')
parser.add_argument('input2', help='second input file')
args = parser.parse_args()

filter_dict = dh.convert_filter_list_to_dic(args.filter_list)
dict_cases = dh.convert_filter_list_to_dic(args.list_cases)
case_info = list(dict_cases.keys())

con1 = dh.read_json_file(args.dbo, args.input, filter_dict, case_info, prop.VALUE_INFO)
con2 = dh.read_json_file(args.dbo, args.input2, filter_dict, case_info, prop.VALUE_INFO)

agg = da.aggregate_data(con1, con2, 'auto', 'time_op')

pickle.dump(agg, open('.agg_data.pkl', 'wb'), pickle.HIGHEST_PROTOCOL)
