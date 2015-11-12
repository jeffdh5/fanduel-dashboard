import datetime
import json
import os

"""
Config methods
"""
CONFIG_PATH = "scraper_config.json"

def load_config():
	config = json.loads(open(CONFIG_PATH, 'r').read())
	return config

def get_fd_pipe_in_fname():
	date_str = datetime.datetime.strftime(get_curr_date(), '%m-%d-%Y')
	config = load_config()
	base_path = config['scraper_base_path']
	pipeline_in = config['pipeline_in']
	fname = 'fanduel_players_' + date_str + '.csv'
	#print os.path.join(base_path, pipeline_in, fanduel_file_name)
	return os.path.join(base_path, pipeline_in, fname)

def get_fd_pipe_out_fname():
	date_str = datetime.datetime.strftime(get_curr_date(), '%m-%d-%Y')

	config = load_config()
	#print(config)

	base_path = config['scraper_base_path']
	pipeline_out = config['pipeline_out']
	fname = 'fanduel_players_' + date_str + '.json'
	#print os.path.join(base_path, pipeline_out, fanduel_file_name)
	return os.path.join(base_path, pipeline_out, fname)

def get_daily_lineup_out_fname():
	date_str = datetime.datetime.strftime(get_curr_date(), '%m-%d-%Y')
	config = load_config()
	base_path = config['scraper_base_path']
	pipeline_out = config['pipeline_out']
	fname = 'daily_lineups' + date_str + '.json'
	return os.path.join(base_path, pipeline_out, fname)

def get_acronym_mapping_in_fname():
	config = load_config()
	base_path = config['scraper_base_path']
	fname = config['acronym_mapping_in']
	return os.path.join(base_path, fname)

def get_acronym_mapping_out_fname():
	config = load_config()
	base_path = config['scraper_base_path']
	fname = config['acronym_mapping_out']
	return os.path.join(base_path, fname)

def get_schedule_in_fname():
	config = load_config()
	base_path = config['scraper_base_path']
	fname = config['schedule_in']
	return os.path.join(base_path, fname)

def get_schedule_out_fname():
	config = load_config()
	base_path = config['scraper_base_path']
	fname = config['schedule_out']
	return os.path.join(base_path, fname)


"""
Time methods
"""

def get_curr_date():
	now = datetime.datetime.now()
	if now.hour >= 16:
		now = now + datetime.timedelta(days=1)
	today = now.replace(hour=0, minute=0, second=0, microsecond=0)
	return today

def get_curr_time():
	now = datetime.datetime.now()
	return now

"""
Data cleaning methods
"""



"""
Data parsing methods
"""

# Used to parse the daily lineup / depth chart data
# Converts the player names into player objects
def parse_team_depth(depth_dict):
	position_player_map = depth_dict['positions']
	injured = set(depth_dict['injured'])

	for position in position_player_map:
		# Initially, these players will be simply represented as strings containing
		# only their name. This function will convert those strings into Player
		# instances.
		players = position_player_map[position]
		for c in range(len(players)):

			# @TODO: Create a function who's job is to populate the player_dict 
			#print(players)
			player_name = players[c]
			player = Player(player_name)
			players[c] = player
			player.set_property('position', position)
			if player_name in injured:
				player.set_property('is_injured', True)

	return depth_dict


# Used to parse the output of daily lineup pipeline, and wrap inside data structures
# defined inside of util.py
def parse_games(raw_games):
	games = []
	for raw_game in raw_games:
		# STEP 1: Convert player name strings into player objects
		home_team_dict = parse_team_depth(raw_game['home_depth'])
		home_team_dict['name'] = raw_game['home']
		away_team_dict = parse_team_depth(raw_game['away_depth'])
		away_team_dict['name'] = raw_game['away']

		# STEP 2: Wrap team JSON data inside Team data structure
		home = Team(home_team_dict)
		away = Team(away_team_dict)

		# STEP 3: Wrap game JSON data inside Game data structure
		game = Game(home, away, raw_game['date'])
		games.append(game)
	return games

"""
Misc
"""

def calculate_fanduel_score(score_dict):
	pass



"""
Lower Level Base Class Definitions
"""

class Player:
	def __init__(self, player_name):

		self.player_dict = {}
		self.comments = []
		self.set_property('name', player_name)
		self.set_property('is_injured', False)

	def get_name(self):
		if 'name' in self.player_dict:
			return self.player_dict['name']
		raise Exception

	def get_age(self):
		if 'age' in self.player_dict:
			return self.player_dict['age']
		raise Exception

	def get_height(self):
		if 'height' in self.player_dict:
			return self.player_dict['height']
		raise Exception

	def get_position(self):
		if 'position' in self.player_dict:
			return self.player_dict['position']

	def set_property(self, prop_key, prop_val):
		self.player_dict[prop_key] = prop_val

	def get_property(self, prop_key):
		if prop_key in self.player_dict:
			return self.player_dict[prop_key]

	def get_properties(self):
		return self.player_dict

	def as_json(self):
		return {'player_data': self.player_dict, 'player_comments': self.comments}

class Team:
	def __init__(self, team_dict):
		assert type(team_dict) == dict
		assert 'positions' in team_dict
		assert 'name' in team_dict
		self.team_dict = team_dict
		self.comments = []

		# Mapping from player names to player objects
		# Invoked by get methods below
		self.player_map = {}

		for position in self.team_dict['positions']:
			players = self.team_dict['positions'][position]
			for player in players:
				self.player_map[player.get_name()] = player

	def get_players(self):
		return [item[1] for item in self.player_map.items()]

	def get_player_names(self):
		return self.player_map.keys()

	def get_player_by_name(self, player_name):
		if name in self.player_map:
			return self.player_map[player_name]

	def get_depth(self):
		return self.team_dict['positions']

	def get_injured(self):
		return self.team_dict['injured']

	def set_property(self, prop_key, prop_val):
		self.team_dict[prop_key] = prop_val

	def get_property(self, prop_key):
		return self.team_dict[prop_key]

	def as_json(self):
		json_team_dict = {}
		json_team_dict['positions'] = {}
		for position in self.team_dict['positions']:
			json_team_dict['positions'][position] = []
			for player in self.team_dict['positions'][position]:
				json_team_dict['positions'][position].append(player.as_json())

		for key in self.team_dict:
			if key != 'positions':
				json_team_dict[key] = self.team_dict[key]

		json_team_dict['team_comments'] = self.comments
		return json_team_dict

	def get_core_lineup(self, as_json=False):
		core_lineup = []
		for position in self.team_dict['positions']:
			players = self.team_dict['positions'][position]
			if as_json:
				core_lineup.append(players[0].as_json())
			else:
				core_lineup.append(players[0])
		return core_lineup


class Game:
	def __init__(self, home_team, away_team, date, referees=[]):

		self.home = home_team
		self.away = away_team
		self.date = date
		self.referees = referees
		self.comments = []

	def get_home_depth(self):
		return self.home

	def get_away_depth(self):
		return self.away

	def get_player(self, player_name):
		if self.home.get_player(player_name):
			return self.home.get_player(player_name)
		if self.away.get_player(player_name):
			return self.away.get_player(player_name)

	def as_json(self):
		return {
			'date': self.date,
			'referees': self.referees,
			'game_comments': self.comments, 
			'home': self.home.as_json(), 
			'away': self.away.as_json()
		}

	def get_game_key(self):
		return self.home.get_property('name') + '@' + self.away.get_property('name')

	# Current algorithm is really dumb, just gets first player in depth chart of each player
	# @TODO: Make this an estimated lineup based off of past data
	def get_core_lineups(self, as_json=False):
		home_core = self.home.get_core_lineup(as_json=as_json)
		away_core = self.away.get_core_lineup(as_json=as_json)
		return {'home': home_core, 'away': away_core}


