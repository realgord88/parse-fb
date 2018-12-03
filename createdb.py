import sqlite3
conn = sqlite3.connect('example.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE users (url TEXT, post TEXT, likes TEXT, comments TEXT, date TEXT)''')
conn.commit()
c.close()
conn.close()
