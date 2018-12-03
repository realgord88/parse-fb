import dryscrape
import sys
import time
import re
import sqlite3

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

if 'linux' in sys.platform:
	dryscrape.start_xvfb()

parse_urls:
	login_fb = '123'
	password_fb = '123'
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
