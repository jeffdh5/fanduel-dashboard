from scraper import lineup_analyzer

class GameDataLoader:

	QUERY_URL_BASE = '/query'

	def __init__(self):
		self.lineup_analyzer = lineup_analyzer.LineupAnalyzer()

	def load_game_schedule(self):
		games = self.lineup_analyzer.get_games()
		game_schedule = []
		for game in games:
			key = game.get_game_key()
			game = game.as_json()
			game_schedule.append({'home': game['home']['name'], 'away': game['away']['name'], 'query_url':self.QUERY_URL_BASE+'/'+key})
		return game_schedule

	def get_game_data(self, game_key):
		game = self.lineup_analyzer.get_game_by_key(game_key)
		return game.as_json()

	def get_core_lineups(self, game_key):
		game = self.lineup_analyzer.get_game_by_key(game_key)
		return game.get_core_lineups(as_json=True)

"""
game_data_loader = GameDataLoader()
game = game_data_loader.load_game_schedule()[0]
key = game['query_url'].split('/')[-1]
print(game_data_loader.get_core_lineups(game_key=key)['home'])
"""