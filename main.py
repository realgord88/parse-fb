import dryscrape
import sys
import time
import re
import sqlite3
import subprocess
import os


conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

def scrape_urls():
	if 'linux' in sys.platform:
		dryscrape.start_xvfb()
	login_fb = '' #your login
	password_fb = '' #your password
	sess = dryscrape.Session()
	sess.set_attribute('auto_load_images', False)
	sess.visit('https://www.facebook.com')
	login = sess.at_xpath('//*[@id="email"]')
	password = sess.at_xpath('//*[@id="pass"]')
	login.set(login_fb)
	password.set(password_fb)
	login.form().submit()
	sess.visit('https://www.facebook.com/natasha.petrova.50')
	print('logged')

	for i in range(1, 1100):
		sess.exec_script("window.scrollTo(0, document.body.scrollHeight);")
		print('Scrole ' + str(i) + ' of 1100')
		time.sleep(4)
	print('scrolled')


	urls = open('urls.txt', 'w')
	for url in sess.xpath('//*[@class="_5pcq"]'):
		url = url['href']
		if url.find('/pages/') == -1:
			if url[0] == '/':
				urls.write('https://www.facebook.com' + url + '\n')
			else:
				urls.write(url+'\n')


def scrape_post():
	if 'linux' in sys.platform:
		dryscrape.start_xvfb()
	login_fb = '122'
	password_fb = '122'
	sess = dryscrape.Session()
	sess.set_attribute('auto_load_images', False)
	sess.visit('https://www.facebook.com')
	login = sess.at_xpath('//*[@id="email"]')
	password = sess.at_xpath('//*[@id="pass"]')
	login.set(login_fb)
	password.set(password_fb)
	login.form().submit()
	print('logged')

	urls = open('urls.txt', 'r')
	line = urls.readline()

	counter = 1
	check_memory = 0

	while line:
		check_memory +=1
		if check_memory % 10 == 0:
			sess.reset()
			login_fb = '1212'
			password_fb = '1212'
			sess = dryscrape.Session()
			sess.set_attribute('auto_load_images', False)
			sess.visit('https://www.facebook.com')
			login = sess.at_xpath('//*[@id="email"]')
			password = sess.at_xpath('//*[@id="pass"]')
			login.set(login_fb)
			password.set(password_fb)
			login.form().submit()

		progress = open('progress.txt', 'w')
		
		full_adress = line[:-1]
		sess.visit(full_adress)
		print(full_adress)

		date = sess.xpath('//*[@class="_5pcq"]/abbr')
		date = date[0]["title"]

		try:
			likes = sess.xpath('//*[@class="_4arz"]/span')
			likes = likes[0].text()
		except:
			likes = 0

		try:
			content = sess.xpath('//*[@class="_5pbx userContent"]/*')
			content = re.sub("^\s+|\n|\r|\t|'|\|/|\s+$", '', content[0].text())
		except:
			content = 'Photo/Repost'

		body = str(sess.body())
		comments = body.count('class="livetimestamp"')

		conn.execute("insert into users (url, post, likes, comments, date) values (?, ?, ?, ?, ?)", (str(full_adress), str(content), str(likes), str(comments), str(date) ))
		conn.commit()

		line = urls.readline()
		print(str(counter) + ' of ' + '98')

		counter += 1
		progress.write(str(counter) + '\n')
		
			
scrape_urls()
scrape_post()

progress.close()
c.close()
conn.close()
