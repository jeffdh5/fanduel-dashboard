import sqlite3
from util import get_curr_date
import util
import numpy as np
import os

config = util.load_config()
base_path = config['scraper_base_path']
DB_FILE = os.path.join(base_path, config['players_feed_out'])

class PlayerQueryEngine:

	# 'PTS': points
	# 'MP': minutes played
	# 'BL': blocks
	# 'A': assists
	# 'S': steals
	# 'TOT': total rebounds
	# 'TOV': turnovers
	DEFAULT_QUERY_STATS = ['Date', 'opp_team', 'MP', 'PTS', 'TOT', 'A', 'ST', 'BL', 'TOV', 'FPS']

	def __init__(self, db_file=DB_FILE):
		print(DB_FILE)
		self.db_file = DB_FILE

		self.conn = sqlite3.connect(DB_FILE)
		self.cursor = self.conn.cursor()

	def get_last_n_stats(self, player_name, n=5, query_stats=None):
		if not query_stats:
			query_stats = self.DEFAULT_QUERY_STATS

		today = get_curr_date()
		select_stats = ''

		# @TODO: Design a way so that you can easily tell what type a column is in your database
		# Right now, we're explicitly checking for the date so that we don't convert it to float
		# representation
		for stat in query_stats:
			select_stats += stat + ', '

		
		#Truncate extra comma and space at end, if there was at least one entry for query stats
		if len(query_stats) > 0:
			select_stats = select_stats[0:-2]
		
		template = 'SELECT ' + select_stats + ' FROM player_stats WHERE name = ? and date <= ? ORDER BY date DESC LIMIT ? '
		results = self.cursor.execute(template, [player_name, today, n]).fetchall()
		total = 0
		for row in results:
			total += row[-1]
		print total/5
		return results

	def get_last_n_averaged_stats(self, player_name, n=5, query_stats=None):
		if not query_stats:
			query_stats = self.DEFAULT_QUERY_STATS

		today = get_curr_date()
		last_n_stats = np.array(self.get_last_n_stats(player_name, n, query_stats))
		indices = [i for i in range(len(query_stats)) if query_stats[i] != 'Date' and query_stats[i] != 'opp_team']
		last_n_stats = last_n_stats[:, indices].astype(float)
		avgs = list(np.mean(last_n_stats, axis=0))
		avgs = [round(avg, 2) for avg in avgs]
		print(avgs)
		return avgs

		"""
		select_stats = ''
		for stat in query_stats:
			if stat.lower() != 'date' and stat.lower() != 'opp_team':
				#select_stats += 'printf("%.2f", avg(' + stat + ')), '
				select_stats += 'avg(' + stat + '), '
			if stat.lower() == 'date':
				select_stats += 'date, '
		
		#Truncate extra comma and space at end, if there was at least one entry for query stats
		if len(query_stats) > 0:
			select_stats = select_stats[0:-2]

		template = 'SELECT ' + select_stats + ' FROM player_stats WHERE name = ? and date <= ? ORDER BY date DESC LIMIT ?'
		results = self.cursor.execute(template, [player_name, today, n]).fetchone()
		#return np.array(results, dtype=np.float32)
		results = [round(r, 2) for r in results if type(r) == float]
		"""

		#return results

	def get_last_n_stats_std(self, player_name, n=5, query_stats=None):

		if not query_stats:
			query_stats = self.DEFAULT_QUERY_STATS

		indices = []
		for c in range(len(query_stats)):
			stat = query_stats[c]
			if stat.lower() != 'date' and stat.lower() != 'opp_team':
				indices.append(c)

		last_n_stats = self.get_last_n_stats(player_name, n=5, query_stats=query_stats)
		cleaned_stats = []
		for row in last_n_stats:
			cleaned_row = [row[i] for i in indices]
			cleaned_stats.append(cleaned_row)

		cleaned_stats = np.array(cleaned_stats, dtype=np.float32)

		stds = np.std(cleaned_stats, axis=0).tolist()
		stds = [round(std, 2) for std in stds]
		return stds


engine = PlayerQueryEngine()
print engine.get_last_n_stats('Klay Thompson')
#print engine.get_last_n_stats_std('Stephen Curry')
#print engine.get_last_n_averaged_stats('Stephen Curry')