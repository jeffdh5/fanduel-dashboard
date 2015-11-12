from bs4 import BeautifulSoup
import urllib2
import sanitizer

URL = 'http://www.rotoworld.com/teams/depth-charts/nba.aspx'
sanitizer = sanitizer.Sanitizer()

def scrape_depth_chart():
	req = urllib2.Request(URL)
	response = urllib2.urlopen(req)
	the_page = response.read()

	soup = BeautifulSoup(the_page, 'html.parser')

	depth_chart_html = soup.find(id="cp1_tblDepthCharts")

	# th tags correspond to team names, the text of the team names are found inside the first
	# url of the th tag
	th = depth_chart_html.find_all("th")
	team_names = [sanitizer.sanitize_team_name(namelink.find('a').text) for namelink in th]
	# get tables corresponding to teams
	tables = depth_chart_html.find_all("table")

	team_depth_charts = {}

	for c in range(len(tables)):
		table = tables[c]
		positions = {}
		injured = []

		table_rows = table.find_all('tr')

		curr_position = None
		curr_position_players = []
		for row in table_rows:
			tds = row.find_all('td')
			if tds[0].text != '':
				next_position = row.find_all('td')[0].text
				if next_position != '':
					if curr_position and row.find_all('td')[0].text != curr_position:
						positions[curr_position] = curr_position_players
						curr_position_players = []
					curr_position = next_position
			player_name = tds[1].find('a').text
			curr_position_players.append(player_name)

			# website provides an image tag that tells you if player is sidelined/out
			is_sidelined = tds[1].find('img') != None
			if is_sidelined:
				injured.append(player_name)

		# need to fill up one last time, or else nonempty curr_position_players array data will get tossed
		positions[curr_position] = curr_position_players

		team_depth_charts[team_names[c]] = {'injured': injured, 'positions': positions}
		#print(positions)
		#print(injured)

	return team_depth_charts

if __name__ == '__main__':
	scrape_depth_chart()
