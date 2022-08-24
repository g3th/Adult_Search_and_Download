import requests
import time
from bs4 import BeautifulSoup as soup
from header import title
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

title()
blacklist = ['https://www.pornpics.com/terms/', 'https://www.pornpics.com/privacy/', 'https://www.pornpics.com/cookie/', 'https://www.pornpics.com/dmca/', 'https://www.pornpics.com/2257/', 'https://www.pornpics.com/parents/', 'https://www.pornpics.com/contact/', 'https://www.pornpics.com/feedback/', 'https://www.pornpics.com/contact/', 'https://www.pornpics.com/jobs/', 'https://www.pornpics.com/cookie/','https://www.pornpics.com/feedback/']

tiles = []
links = []
page = 'https://www.pornpics.com/pornstars/'
query = input('Enter search term: ')
browser_options = Options()
browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
browser_options.headless = True
browser = webdriver.Chrome(options = browser_options)
browser.get(page+query)
counter = 0

while counter != 2:
	print('Fetching Images..')
	html = browser.find_element_by_tag_name('html')
	html.send_keys(Keys.END)
	time.sleep(0.9)
	counter +=1

for link in browser.find_elements_by_tag_name('a'):
	temporary_link = link.get_attribute('href')
	if 'galleries' not in str(temporary_link):
		pass
	else:
		tiles.append(link.get_attribute('href'))

while True:
	try:
		print('\x1bc Fetched a Total of {} galleries'.format(len(tiles)))
		user_photo_number_choice = int(input('How many galleries would you like to download?'))
		if user_photo_number_choice > len(tiles):
			continue
		else:
			break
	except ValueError:
		continue

for gallery in range(user_photo_number_choice):
	request = requests.get(tiles[gallery])
	fetch_galleries = soup(request.content, 'html.parser')
	parse_links = fetch_galleries.find_all('a',{'class':'rel-link'})
	for link in parse_links:
		print(link['href'])
