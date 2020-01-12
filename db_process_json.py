import pjr.DBHelper as dh
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('db_path', help='Path to the database')
parser.add_argument('json_path', help='Path to the json file')
args = parser.parse_args()

dh.read_json_file_raw(args.db_path, args.json_path)

