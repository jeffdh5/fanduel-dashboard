from bottle import route, run, static_file
import json
import os
import datetime
from scraper import game_data_loader
from scraper import lineup_analyzer

loader = game_data_loader.GameDataLoader()

def filter_pool(player_pool):
	TEAM_TARGET = 280.
	FD_TOTAL = 60000.
	TARGET_COST_PER_FP = FD_TOTAL/TEAM_TARGET
	filtered_pool = []

	for player in player_pool:
		#print(player.player_dict)
		fppg = player.get_property('FPPG') 
		salary = player.get_property('fanduel_salary')
		if fppg == None or salary == None:
			lineup_analyzer.fanduel_data_perspective(player)
		
		fppg = player.get_property('FPPG') 
		salary = player.get_property('fanduel_salary')
		if fppg != None and fppg > 0 and salary != None:
			print("here")
			target_value = salary / TARGET_COST_PER_FP
			if fppg >= 0.9 * target_value:
				filtered_pool.append(player)

	return filtered_pool

def sort_pool(player_pool):

	TEAM_TARGET = 280.
	FD_TOTAL = 60000.
	TARGET_COST_PER_FP = FD_TOTAL/TEAM_TARGET

	def calc_percentage_over_target(player):
		fppg = player.get_property('FPPG')
		salary = player.get_property('fanduel_salary')
		print(fppg, salary)
		target_value = salary / TARGET_COST_PER_FP
		return (fppg-target_value)/target_value


	sorted_pool = sorted(player_pool, key=calc_percentage_over_target, reverse=True)
	return sorted_pool



@route('/')
def index():
	return static_file('index.html', '')

@route('/todays_games')
def query_todays_games():
	return json.dumps(loader.load_game_schedule())

@route('/player_pool')
def get_player_pool():
	player_pool = []
	for game in loader.lineup_analyzer.games:
		for player in game.home.get_players():
			player_pool.append(player)
		for player in game.away.get_players():
			player_pool.append(player)
	player_pool = filter_pool(player_pool)
	player_pool = sort_pool(player_pool)
	player_pool = [player.as_json() for player in player_pool]
	return json.dumps(player_pool)

@route('/query/<game_key>/core_lineup')
def query_core_lineup(game_key):
	#game_key = game_key.replace('-', '/')
	core_lineup = loader.get_core_lineups(game_key)

	return json.dumps(core_lineup)

@route('/query/<game_key>')
def query_game_data(game_key):
	#game_key = game_key.replace('-', '/')
	game = loader.get_game_data(game_key)
	return json.dumps(game_data)

@route('/<filename:re:.*\.js>')
def send_js(filename):
	print("here")
	return static_file(filename, '')

run(host='localhost', port=8080, debug=True)

#print query_core_lineup('GSW@HOU10/30/2015')
