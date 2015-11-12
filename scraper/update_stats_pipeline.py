import sqlite3
import os
import xlrd
import util


#fname = 'pipeline_in/season-player-feed.xlsx'

config = util.load_config()
base_path = config['scraper_base_path']
fname = os.path.join(base_path, config['players_feed_in'])

db = os.path.join(base_path, util.load_config()['players_feed_out'])


xl_workbook = xlrd.open_workbook(fname)
xl_sheet = xl_workbook.sheet_by_index(0)
row = xl_sheet.row(0) 
nrows = xl_sheet.nrows
#print row

data = []
for c in range(1, nrows):
	row = xl_sheet.row(c)
	row_values = []
	for r in row:
		row_values.append(r.value)

	rebounds = row_values[16]
	assists = row_values[17]
	steals = row_values[19]
	turnovers = row_values[20]
	blocks = row_values[21]
	pts = row_values[22]
	fantasy_points = (rebounds*1.2) + (assists*1.5) + (blocks*2) + (steals*2) + pts - turnovers

	row_values.append(fantasy_points)
	data.append(row_values)

row = xl_sheet.row(1)
for r in range(len(row)):
	print(r, row[r])

table_exists = True

conn = sqlite3.connect(db)
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS player_stats''')
c.execute('''CREATE TABLE player_stats (dataset text, date text, name text, position text, own_team text, opp_team text, venue text, MP real, FG integer, FGA integer, TP integer, TPA integer, FT integer, FTA integer, OReb integer, DReb integer, TOT integer, A integer, PF integer, ST integer, TOV integer, BL integer, PTS integer, FPS integer)''')
c.executemany('INSERT INTO player_stats VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?, ?, ?, ?)', data)

conn.commit()
conn.close()