##################################### Method 1
import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
import os


def merge_stories(news, shaded_news):
	c = 0
	merged = []
	while c < len(news) or c < len(shaded_news):
		if c < len(news):
			merged.append(news[c])
		if c < len(shaded_news):
			merged.append(shaded_news[c])
		c += 1
	return merged

def rotowire_news_scraper(html_doc):
	soup = BeautifulSoup(html_doc, 'html.parser')
	raw_stories = soup.findAll(class_='span34 news-item')
	raw_stories_shaded = soup.findAll(class_='span34 news-item-shaded')
	raw_stories = merge_stories(raw_stories, raw_stories_shaded)
	cleaned_stories = []
	for story in raw_stories:
		try:
			date = story.find(class_ ='offset1').find(class_='news-item-date').text
			story_data = story.find(class_='span28')
			player_name = story_data.findAll(class_='news-player')[0].find('a').text.strip()
			update = story_data.findAll(class_='news-item-news')[0].text.strip()
			analysis = story_data.findAll(class_='news-item-analysis')[0].text.strip().split('\r\n\t\t\t\t\t\t')[1]
			player_name = remove_nonascii(player_name)
			update = remove_nonascii(update)
			analysis = remove_nonascii(analysis)
			cleaned_stories.append((player_name, date, update, analysis))
		except Exception as e:
			#print("Failed")
			print(e)
			pass
	cleaned_stories.reverse()
	return cleaned_stories


def get_last_n_stories(story_log, n=50):
	old_stories = []
	while len(story_log) >= 5 and n > 0:
		story = tuple([l.strip() for l in story_log[-5:-1]])
		story_log = story_log[0:-5]
		old_stories.append(story)
		n = n-1
	return old_stories

def remove_nonascii(text):
	return ''.join([i if ord(i) < 128 else '' for i in text])

def write_rotowire_data(out_fname, data):
	last_n_scraped_stories = []
	if os.path.exists(out_fname):
		f = open(out_fname)
		story_log = f.readlines()
		f.close()
		last_n_scraped_stories = get_last_n_stories(story_log, 50)

	f = open(out_fname, 'a')
	oldest_story_unwritten = data[0]
	print(oldest_story_unwritten)
	for c in range(len(last_n_scraped_stories)):
		scraped_story = last_n_scraped_stories[c]
		#print('oldest', oldest_story_unwritten)
		#print('scraped', scraped_story)
		if oldest_story_unwritten == scraped_story: 
			print('col')
			data = data[c+1:]
			break
		c += 1

	for story in data:
		player_name, date, update, analysis = story
		f.write(player_name + '\n')
		f.write(date + '\n')
		f.write(update + '\n')
		f.write(analysis + '\n')
		f.write('\n')

	f.close()

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
br.open('http://rotowire.com')

br.select_form(nr=0)
br.form['username'] = 'jeffdh5'
br.form['p1'] = 'isuckcock'

# Login
br.submit()

#Scrape injuries
html_doc = br.open('http://www.rotowire.com/basketball/injuries.htm').read()
data = rotowire_news_scraper(html_doc)
write_rotowire_data('injuries.txt', data)

#Scrape general news
html_doc = br.open('http://www.rotowire.com/basketball/latestnews.htm').read()
data = rotowire_news_scraper(html_doc)
write_rotowire_data('news.txt', data)


