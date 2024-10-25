import sqlite3
import csv

# Create or connect to SQLite database
conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

# Create the sales table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    product_id INTEGER,
    store_id INTEGER,
    quantity INTEGER
)
''')

# Open CSV file and insert data into the table
with open('sales.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader) 
    for row in reader:
        cursor.execute('INSERT INTO sales (date, product_id, store_id, quantity) VALUES (?, ?, ?, ?)', row)

# Commit and close the connection
conn.commit()
conn.close()
