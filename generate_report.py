import datetime
from scraper import game_data_loader, lineup_analyzer

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
			if fppg >= .85 * target_value:
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
			
		val = (fppg-target_value)/target_value
		if player.get_property('is_injured') == True:
			return val-10000
		else:
			return val

	sorted_pool = sorted(player_pool, key=calc_percentage_over_target, reverse=True)
	return sorted_pool


def get_player_pool():
	player_pool = []
	for game in loader.lineup_analyzer.games:
		for player in game.home.get_players():
			player_pool.append(player)
		for player in game.away.get_players():
			player_pool.append(player)
	player_pool = filter_pool(player_pool)
	player_pool = sort_pool(player_pool)
	return player_pool

def write_report(player_pool):

	TEAM_TARGET = 280.
	FD_TOTAL = 60000.
	TARGET_COST_PER_FP = FD_TOTAL/TEAM_TARGET

	lines = []
	for player in player_pool:

		name = player.get_property('name')
		salary = player.get_property('fanduel_salary')
		if salary <= 5000:
			position = player.get_property('position')
			games_headers = ['Date', 'OPP', 'PTS', 'MP', 'BS', 'A', 'ST', 'REB', 'TO', 'FPS']
			stat_headers = ['PTS', 'MP', 'BS', 'A', 'ST', 'REB', 'TO', 'FPS']
			fppg = player.get_property('FPPG')
			target = salary / TARGET_COST_PER_FP
			last_five_stats = player.get_property('last_5_games')
			last_five_std = player.get_property('last_5_games_std')
			last_five_avg = player.get_property('last_5_games_avg')
			is_injured = player.get_property('is_injured')

			last_ten_stats = player.get_property('last_10_games')
			last_ten_std = player.get_property('last_10_games_std')
			last_ten_avg = player.get_property('last_10_games_avg')
			line = name + ' | Position: ' + position + ' | Salary: ' + str(salary) + ' | FPPG: ' + str(fppg) + ' | Target: ' + str(target)
			if is_injured:
				line += ' | INJURED'
			if last_five_avg:
				line += ' | L5 FPPG: ' + str(last_five_avg[-1])
				line += ' | L5 STD: ' + str(last_five_std[-1])

			lines.append(line)
			lines.append('\n')
			lines.append('\n')

	f = open("report_cheap.txt", 'w+')
	for line in lines:
		f.write(line)
	f.close()

	lines = []
	for player in player_pool:

		name = player.get_property('name')
		salary = player.get_property('fanduel_salary')
		if salary > 5000 and salary < 8900:
			position = player.get_property('position')
			games_headers = ['Date', 'OPP', 'PTS', 'MP', 'BS', 'A', 'ST', 'REB', 'TO', 'FPS']
			stat_headers = ['PTS', 'MP', 'BS', 'A', 'ST', 'REB', 'TO', 'FPS']
			fppg = player.get_property('FPPG')
			target = salary / TARGET_COST_PER_FP
			last_five_stats = player.get_property('last_5_games')
			last_five_std = player.get_property('last_5_games_std')
			last_five_avg = player.get_property('last_5_games_avg')
			is_injured = player.get_property('is_injured')

			last_ten_stats = player.get_property('last_10_games')
			last_ten_std = player.get_property('last_10_games_std')
			last_ten_avg = player.get_property('last_10_games_avg')
			line = name + ' | Position: ' + position + ' | Salary: ' + str(salary) + ' | FPPG: ' + str(fppg) + ' | Target: ' + str(target)
			if is_injured:
				line += ' | INJURED'
			if last_five_avg:
				line += ' | L5 FPPG: ' + str(last_five_avg[-1])
				line += ' | L5 STD: ' + str(last_five_std[-1])


			lines.append(line)
			lines.append('\n')
			lines.append('\n')

	f = open("report_medium.txt", 'w+')
	for line in lines:
		f.write(line)
	f.close()

	lines = []
	for player in player_pool:

		name = player.get_property('name')
		salary = player.get_property('fanduel_salary')
		if salary >= 8900:
			position = player.get_property('position')
			games_headers = ['Date', 'OPP', 'PTS', 'MP', 'BS', 'A', 'ST', 'REB', 'TO', 'FPS']
			stat_headers = ['PTS', 'MP', 'BS', 'A', 'ST', 'REB', 'TO', 'FPS']
			fppg = player.get_property('FPPG')
			target = salary / TARGET_COST_PER_FP
			last_five_stats = player.get_property('last_5_games')
			last_five_std = player.get_property('last_5_games_std')
			last_five_avg = player.get_property('last_5_games_avg')
			is_injured = player.get_property('is_injured')

			last_ten_stats = player.get_property('last_10_games')
			last_ten_std = player.get_property('last_10_games_std')
			last_ten_avg = player.get_property('last_10_games_avg')
			line = name + ' | Position: ' + position + ' | Salary: ' + str(salary) + ' | FPPG: ' + str(fppg) + ' | Target: ' + str(target)
			if is_injured:
				line += ' | INJURED'
			if last_five_avg:
				line += ' | L5 FPPG: ' + str(last_five_avg[-1])
				line += ' | L5 STD: ' + str(last_five_std[-1])


			lines.append(line)
			lines.append('\n')
			lines.append('\n')

	f = open("report_expensive.txt", 'w+')
	for line in lines:
		f.write(line)
	f.close()



pool = sort_pool(filter_pool(get_player_pool()))
write_report(pool)




