import sqlite3
import random
from string import ascii_lowercase

conn = sqlite3.connect("database.db",check_same_thread=False)

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS keys
(key TEXT NOT NULL UNIQUE,active INTEGER)
""")

def keygen():
	key = []
	for i in range(5):
		key.append(str(random.randint(0,9)))
	for i in range(5):
		key.append(random.choice(ascii_lowercase))
	return "".join(key)

def updatedb(array):
	for key in array:
		cursor.execute(f"""INSERT INTO keys VALUES ("{key}",0)""")
	conn.commit()

def getallkeys():
	data = cursor.execute("""SELECT key FROM keys""").fetchall()
	data = {k[0] for k in data}
	return data

def getkeyactivity(key):
	try:
		return cursor.execute(f'SELECT active FROM keys WHERE key = "{key}"').fetchone()[0]
	except:
		return 99

def setkeyactivity(key,activity):
	cursor.execute(f'UPDATE keys SET active = {activity} WHERE key = "{key}"')
	conn.commit()

def clearactivity():
	cursor.execute(f"UPDATE keys SET active = 0")
	conn.commit()

k_array = []
for i in range(99):
	k_array.append(keygen())


"""
print(getkeyactivity("99721isurk"))
setkeyactivity("99721isurk",1)
print(getkeyactivity("99721isurk"))
"""