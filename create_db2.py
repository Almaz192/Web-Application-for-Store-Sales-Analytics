import sqlite3
import csv

# Create or connect to SQLite database
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Create the products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    product TEXT,
    price INTEGER
)
''')

# Open CSV file and insert data into the table
with open('products.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        cursor.execute('INSERT INTO products (id, product, price) VALUES (?, ?, ?)', row)

# Commit and close the connection
conn.commit()
conn.close()
