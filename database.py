import sqlite3

def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, item TEXT, quantity INTEGER)''')
    conn.commit()
    conn.close()

def save_order(order):
    with sqlite3.connect('orders.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO orders (item, quantity) VALUES (?, ?)', (order["item"], order["quantity"]))
        conn.commit()

def get_orders():
    with sqlite3.connect('orders.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM orders')
        orders = c.fetchall()
        headers = ['id', 'item', 'quantity']
        orders_json = []
        for order in orders:
            order_json = dict(zip(headers, order))
            orders_json.append(order_json)
        return orders_json

