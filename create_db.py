import sqlite3
import csv


conn = sqlite3.connect('stores.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS stores (
    id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    working_time TEXT
)
''')


with open('stores.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  
    for row in reader:
        cursor.execute('INSERT INTO stores (id, name, address, working_time) VALUES (?, ?, ?, ?)', row)


conn.commit()
conn.close()
