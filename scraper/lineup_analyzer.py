import daily_lineup_pipeline
from util import get_curr_date, Player, Team, Game, parse_team_depth, parse_games, get_curr_time, load_config
import util
from query_engine import PlayerQueryEngine
import json
import datetime
import os
import datetime


"""
GLOBAL DATA LOADING
"""

fanduel_data_path = util.get_fd_pipe_out_fname()
fanduel_data = json.loads(open(fanduel_data_path, 'r').read())

player_query_engine = PlayerQueryEngine()

def player_stats_perspective(player):
	name = player.get_name()
	player.set_property('last_5_games', player_query_engine.get_last_n_stats(name, n=5))
	if len(player.get_property('last_5_games')) > 0:
		player.set_property('last_5_games_avg', player_query_engine.get_last_n_averaged_stats(name, n=5))
		player.set_property('last_5_games_std', player_query_engine.get_last_n_stats_std(name, n=5))

	# @TODO: Instead of repeating query, just make this query first and choose bottom half of the data
	# and compute the average and std manually that way
	player.set_property('last_10_games', player_query_engine.get_last_n_stats(name, n=10))
	if player.get_property('last_10_games') and len(player.get_property('last_10_games')) > 0:
		player.set_property('last_10_games_avg', player_query_engine.get_last_n_averaged_stats(name, n=10))
		player.set_property('last_10_games_std', player_query_engine.get_last_n_stats_std(name, n=10))

	player.set_property('season_stats', player_query_engine.get_last_n_stats(name, n=82))
	if player.get_property('season') and len(player.get_property('season')) > 0:
		player.set_property('season_avg', player_query_engine.get_last_n_averaged_stats(name, n=82))
		player.set_property('season_std', player_query_engine.get_last_n_stats_std(name, n=82))


def fanduel_data_perspective(player):
	name = player.get_name()
	if name in fanduel_data:
		player.set_property('fanduel_salary', fanduel_data[name]['salary'])
		player.set_property('FPPG', fanduel_data[name]['FPPG'])


def fanduel_hitting_value_perspective(player):
	TEAM_TARGET = 280.
	FD_TOTAL = 60000.
	TARGET_COST_PER_FP = FD_TOTAL/TEAM_TARGET

	# Execute perspective dependencies, if there are any
	if player.get_property('fanduel_salary') == None:
		fanduel_data_perspective(player)
	if player.get_property('season_stats') == None:
		player_stats_perspective(player)



class LineupAnalyzer:

	PERSPECTIVES = {
		'player_context': [player_stats_perspective, fanduel_data_perspective],
		'team_context': [],
		'game_context': []
	}

	def __init__(self):
		self.refresh()

	def refresh(self):
		self.today = get_curr_date()
		self.now = get_curr_time()
		self.load_data()
		self.analyze_games()

	def is_up_to_date(self):
		if get_curr_time()-self.now > datetime.timedelta(minutes=30):
			self.refresh()

	def load_data(self):
		# Constructing the data input		
		data_fname = util.get_daily_lineup_out_fname()
		if not os.path.exists(data_fname):
			daily_lineup_pipeline.run_pipeline()

		f = open(data_fname, 'r')
		raw_games = json.loads(f.read())
		f.close()

		self.games = parse_games(raw_games)
		self.index_games_by_key()

	def index_games_by_key(self):
		self.games_by_key = {}
		for game in self.games:
			self.games_by_key[game.get_game_key()] = game

	def analyze_games(self):
		for game in self.games:
			self.analyze_game(game)

	def analyze_game(self, game):
		for perspective_adder in self.PERSPECTIVES['game_context']:
			perspective_adder(game)

		for perspective_adder in self.PERSPECTIVES['team_context']:
			perspective_adder(game.home)
			perspective_adder(game.away)

		for perspective_adder in self.PERSPECTIVES['player_context']:
			for player in game.home.get_players():
				perspective_adder(player)
			for player in game.away.get_players():
				perspective_adder(player)

	def get_games(self):
		if not self.is_up_to_date():
			self.refresh()
		return self.games

	def get_game_by_key(self, game_key):
		if game_key in self.games_by_key:
			return self.games_by_key[game_key]

#l = LineupAnalyzer()
#print l.games[0].as_json()['home']['team_comments']
