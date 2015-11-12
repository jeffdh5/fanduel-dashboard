import pandas
import json
import os
import sys

PATH = '/'.join(os.getcwd().split('/'))
print(PATH)
import sys
if not PATH in sys.path:
    sys.path.append(PATH)

from scraper import util


"""
Original data:
https://docs.google.com/spreadsheets/d/1Qsr9MNoXeVVo_nHmgQj_omETUhkQp0skgQ5kD_9-GJY/edit#gid=0

(Owner: jeffdh5@gmail.com)
"""

class Sanitizer:

	def __init__(self):
		self.team_mapping = get_team_mapping()

	def sanitize_team_name(self, team_name):
		return self.team_mapping[team_name]


def get_team_mapping():
	ACRONYM_CSV_PATH = util.get_acronym_mapping_in_fname()
	ACRONYM_JSON_PATH = util.get_acronym_mapping_out_fname()
	if os.path.exists(ACRONYM_JSON_PATH):
		return json.loads(open(ACRONYM_JSON_PATH, "r").read())

	mapping_data = open(ACRONYM_CSV_PATH, "r").readlines()
	mapping = {}
	headers = mapping_data[0].split(',')
	official_index = -1
	for c in range(len(headers)):
		if headers[c].lower() == 'official':
			official_index = c
			break

	for row in mapping_data[2:]:
		split_row = row.strip().split(',')
		for acr in split_row:
			if acr != '':
				mapping[acr] = split_row[official_index]
	f = open(ACRONYM_JSON_PATH, "w+")
	f.write(json.dumps(mapping))
	return mapping


if __name__ == '__main__':
	print get_team_mapping()