from misc import schedule_parser
from misc import rotogrinders_depth_chart as depth_chart
import json
import os
from util import get_curr_date
import util
import datetime

def run_pipeline():
	output_fname = util.get_daily_lineup_out_fname()
	now = get_curr_date()

	if not os.path.exists(output_fname):
		team_depth_charts = depth_chart.scrape_depth_chart()
		games = schedule_parser.get_games_on_date(datetime.datetime.strftime(now, '%m/%d/%Y'))
		daily_lineup = []

		for game in games:
			home = game['home']
			away = game['away']
			date = game['date']
			home_depth_data = team_depth_charts[home]
			away_depth_data = team_depth_charts[away]
			daily_lineup_data = {'date': date, 'home': home, 'away': away, 'home_depth': home_depth_data, 'away_depth': away_depth_data}
			daily_lineup.append(daily_lineup_data)


		#now_str = datetime.datetime.strftime(now, '%m-%d-%Y')
		#output_filename = "pipeline_out/daily_lineups_" + now_str + ".json"
		f = open(output_fname, 'w+')
		f.write(json.dumps(daily_lineup, sort_keys=True, indent=4))
		f.close()

