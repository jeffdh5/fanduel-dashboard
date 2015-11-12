"""
Constructs a mapping where the keys are player names, and values are their Fanduel-unique attributes,
such as salary data and average fantasy point values.
"""

from util import get_curr_date
import util
from datetime import datetime
import pandas
import json
import os

now = datetime.strftime(get_curr_date(), '%m-%d-%Y')


def run_pipeline():
	pipeline_in = util.get_fd_pipe_in_fname()
	pipeline_out = util.get_fd_pipe_out_fname()

	if os.path.exists(pipeline_out):
		f = open(pipeline_out, 'r')
		data = json.loads(f.read())
		f.close()
		return data

	player_mapping = {}

	dataframe = pandas.read_csv(pipeline_in)
	nrows = len(dataframe)

	for c in range(nrows):
		curr_player = ' '.join([dataframe['First Name'][c], dataframe['Last Name'][c]])
		fanduel_data = {}
		fanduel_data['salary'] = dataframe['Salary'][c]
		fanduel_data['FPPG'] = dataframe['FPPG'][c]
		player_mapping[curr_player] = fanduel_data

	data = json.dumps(player_mapping, sort_keys=True, indent=4)
	f = open(pipeline_out, 'w+')
	f.write(data)
	f.close()
	return data

run_pipeline()
