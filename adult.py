import requests
import time
import concurrent.futures
import os
from threading import Lock
from pathlib import Path
from bs4 import BeautifulSoup as soup
from header import title
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def threaded_downloads(directory, image_name, images, index):
	with open(directory + image_name,'wb') as download:
		progress = round(index / len(images) * 100, 1)
		print('\rProgress {}    '.format(progress) , end='')
		request = requests.get(images[index])
		download.write(request.content)

directory = str(Path(__file__).parent)+'/downloaded_galleries/'
os.makedirs(directory, exist_ok=True)
title()
blacklist = ['https://www.pornpics.com/terms/', 'https://www.pornpics.com/privacy/', 'https://www.pornpics.com/cookie/', 'https://www.pornpics.com/dmca/', 'https://www.pornpics.com/2257/', 'https://www.pornpics.com/parents/', 'https://www.pornpics.com/contact/', 'https://www.pornpics.com/feedback/', 'https://www.pornpics.com/contact/', 'https://www.pornpics.com/jobs/', 'https://www.pornpics.com/cookie/','https://www.pornpics.com/feedback/']
tiles = []
gallery_images = []
page = 'https://www.pornpics.com/'
query = input('\nEnter search term: ')
full_query = page+'?q='+query.replace(' ','+')
print(full_query)
browser_options = Options()
browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
browser_options.headless = True
browser = webdriver.Chrome(options = browser_options)
browser.get(full_query)
counter = 0

while counter != 5:
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
		title()
		print('Fetched a Total of {} galleries'.format(len(tiles)))
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
		gallery_images.append(link['href'])
mutex = Lock()
with concurrent.futures.ThreadPoolExecutor(20) as executor:
	for image in range(len(gallery_images)):
		executor.submit(threaded_downloads, directory, str(gallery_images[image]).split('_')[2], gallery_images, image)
print('\n')
