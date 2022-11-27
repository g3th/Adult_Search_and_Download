import requests
import time
import concurrent.futures
import os
from pathlib import Path
from bs4 import BeautifulSoup as soup
from header import title
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def threaded_downloads(directory, image_name, images, index):
	with open(directory + image_name,'wb') as download:
		progress = round(index / len(images) * 100, 1)
		print('\rProgress {}    '.format(progress) , end='')
		request = requests.get(images[index])
		download.write(request.content)

directory = str(Path(__file__).parent)+'/downloaded_galleries/'
os.makedirs(directory, exist_ok=True)
title()
tiles = []
gallery_images = []
page = 'https://www.pornpics.com/'
query = input('\nEnter search term: ')
full_query = page+'?q='+query.replace(' ','+')
browser_options = Options()
browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
browser_options.headless = True
browser = webdriver.Chrome(options = browser_options)
browser.get(full_query)
counter = 0

while counter != 5:
	print('Fetching Images..')
	html = browser.page_source
	browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
	time.sleep(0.9)
	counter +=1

for link in browser.find_elements(By.TAG_NAME,"a"):
	temporary_link = link.get_attribute('href')
	if 'galleries' not in str(temporary_link):
		pass
	else:
		tiles.append(link.get_attribute('href'))

while True:
	try:
		title()
		print('Fetched a Total of {} galleries'.format(len(tiles)))
		user_photo_number_choice = int(input('How many galleries would you like to download? '))
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

with concurrent.futures.ThreadPoolExecutor(20) as executor:
	for image in range(len(gallery_images)):
		executor.submit(threaded_downloads, directory, str(gallery_images[image]).split('_')[2], gallery_images, image)
	executor.shutdown()
print('\nAll Done. Total images: {} from {} galleries.\n'.format(len(gallery_images), len(tiles)))
