
from flask import Flask, render_template,request,jsonify
import sqlite3

app = Flask(__name__)

# Route for the main page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Other routes like stores, products, etc. can go here
@app.route('/stores')
def stores():
    conn = sqlite3.connect('stores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    stores = cursor.fetchall()
    conn.close()
    return render_template('stores.html', stores=stores)

# Add products or other routes similarly
@app.route('/products')
def products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/analytics', methods=['GET'])
def sales():
    # Connect to the sales, stores, and products databases
    sales_conn = sqlite3.connect('sales.db')
    cursor = sales_conn.cursor()
    cursor.execute("ATTACH DATABASE 'stores.db' AS stores_db")
    cursor.execute("ATTACH DATABASE 'products.db' AS products_db")

    # Retrieve filter values from the query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    selected_store = request.args.get('store')
    selected_product = request.args.get('product')

    # Get pagination details
    page = int(request.args.get('page', 0))
    per_page = int(request.args.get('per_page', 15))
    offset = page * per_page

    # Base query with joins
    query = '''
    SELECT sales.date, stores_db.stores.name, products_db.products.product, sales.quantity, products_db.products.price
    FROM sales
    JOIN stores_db.stores ON sales.store_id = stores_db.stores.id
    JOIN products_db.products ON sales.product_id = products_db.products.id
    WHERE 1=1
    '''

    # Add filters dynamically based on query parameters
    filters = []
    if start_date:
        query += " AND sales.date >= ?"
        filters.append(start_date)
    if end_date:
        query += " AND sales.date <= ?"
        filters.append(end_date)
    if selected_store:
        query += " AND stores_db.stores.name = ?"
        filters.append(selected_store)
    if selected_product:
        query += " AND products_db.products.product = ?"
        filters.append(selected_product)

    # Add pagination
    query += " LIMIT ? OFFSET ?"
    filters.extend([per_page, offset])

    # Execute the query
    cursor.execute(query, filters)
    sales_data = cursor.fetchall()

    # Query to calculate total sales and total amount
    total_sales_query = '''
    SELECT SUM(sales.quantity), SUM(sales.quantity * products_db.products.price)
    FROM sales
    JOIN products_db.products ON sales.product_id = products_db.products.id
    WHERE 1=1
    '''
    total_filters = []
    if start_date:
        total_sales_query += " AND sales.date >= ?"
        total_filters.append(start_date)
    if end_date:
        total_sales_query += " AND sales.date <= ?"
        total_filters.append(end_date)
    if selected_store:
        total_sales_query += " AND sales.store_id IN (SELECT id FROM stores_db.stores WHERE stores_db.stores.name = ?)"
        total_filters.append(selected_store)
    if selected_product:
        total_sales_query += " AND sales.product_id IN (SELECT id FROM products_db.products WHERE products_db.products.product = ?)"
        total_filters.append(selected_product)

    cursor.execute(total_sales_query, total_filters)
    total_sales, total_sum = cursor.fetchone()

    # Close the database connection
    sales_conn.close()

    # Format the total sales and total sum with commas
    formatted_total_sales = f"{total_sales:,} som"
    formatted_total_sum = f"{total_sum:,} som"

    # Pass the data to the template
    return render_template(
        'analytics.html',
        sales=sales_data,
        total_sales=formatted_total_sales,
        total_sum=formatted_total_sum,
        page=page,
        per_page=per_page,
        start_date=start_date,
        end_date=end_date,
        store=selected_store,
        product=selected_product
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
