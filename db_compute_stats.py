import pjr.DBHelper as dh
import argparse
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('db_path', help='Path to the database')
parser.add_argument('-p', '--prefix', type=str, help='Prefix for the created tables', dest='prefix', default='auto')
parser.add_argument('-l', '--list-cases', type=str, help='list of attributes which will be used to create a case', action='append', dest='list_cases', required=True)
parser.add_argument('-voi', type=str, help='value of interest', dest='voi', required=True)
parser.add_argument('-f', '--filter', type=str, action='append', dest='filter_list')
args = parser.parse_args()

filter_dict = dh.convert_filter_list_to_dic(args.filter_list)
con = sqlite3.connect(args.db_path)
dh.create_filter(con, args.prefix, filter_dict)
dh.create_case_table(con, args.prefix, args.list_cases)
dh.compute_stats(con, args.prefix, args.voi)

