import xlrd
from datetime import datetime
import json
import os
import sanitizer
import sys

PATH = '/'.join(os.getcwd().split('/')[0:-2])
print(PATH)
import sys
if not PATH in sys.path:
    sys.path.append(PATH)


from scraper import util

"""
ORIGINAL URL OF SPREADSHEET: http://rotoguru2.com/hoop/schedule.html
Modifications to original data: Last row is manually removed

"""

SEASON_START = 2015
SEASON_END = 2016

sanitizer = sanitizer.Sanitizer()

def get_schedule_data():
	FILE = util.get_schedule_in_fname()
	OUTPUT_FILE = util.get_schedule_out_fname()

	if os.path.exists(OUTPUT_FILE):
		return json.loads(open(OUTPUT_FILE, 'r').read())

	workbook = xlrd.open_workbook(FILE)
	worksheet = workbook.sheet_by_index(0)

	parsed_data = {}

	#print worksheet.row(0)[0].value
	headers = [cell.value for cell in worksheet.row(0)]
	#print(worksheet.nrows)
	for c in range(1, worksheet.nrows):
		row = worksheet.row(c)
		raw_date = row[0].value
		cleaned_date = raw_date[3:]
		raw_month, raw_day = cleaned_date.strip().split('/')
		month, day = int(raw_month), int(raw_day)

		if month > 8:
			season = SEASON_START
		else:
			season = SEASON_END
		#cleaned_date = datetime.strptime(cleaned_date+'/'+str(season), "%m/%d/%Y")
		cleaned_date = cleaned_date+'/'+str(season)

		games = []

		# ignore last column, its the date column repeated
		for c in range(1, len(row)-1):
			# games are doubled, so only look at the ones where the cell values are away
			if '@' in row[c].value:
				raw_home = headers[c]
				raw_away = row[c].value.strip().lstrip('@ ')
				home = sanitizer.sanitize_team_name(raw_home.upper())
				away = sanitizer.sanitize_team_name(raw_away.upper())

				entry = {"home": home, "away": away, "date": cleaned_date}
				games.append(entry)

		parsed_data[cleaned_date] = games
	f = open(OUTPUT_FILE, 'w+')
	f.write(json.dumps(parsed_data, sort_keys=True, indent=4))
	f.close()
	return parsed_data

def get_games_on_date(date):
	if type(date) != str:
		date = datetime.strptime(date, '%m/%d/%Y')

	data = get_schedule_data()
	#print(data)
	return data[date]

if __name__ == '__main__':
	#get_schedule_data()
	print (get_games_on_date('11/01/2015'))
