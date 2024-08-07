import sqlite3
import datetime

def create_client(name: str, phone: str, email: str, address: str, named_has: str, foreing_id: int):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (name, phone, email, address, named_has, foreing_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, phone, email, address, named_has, foreing_id))
    conn.commit()
    conn.close()
    print(f"Cliente '{name}' creado con éxito.")

def create_product(name: str, description: str, named_has: str, foreing_id: int):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, named_has, foreing_id)
        VALUES (?, ?, ?, ?)
    """, (name, description, named_has, foreing_id))
    conn.commit()
    conn.close()
    print(f"Producto '{name}' creado con éxito.")
# Traer todas las ordenes
def get_all_orders():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    today = datetime.date.today()
    print(today)
    cursor.execute("SELECT * FROM orders WHERE delivery_date = ?", (today,))
    orders = cursor.fetchall()
    conn.close()
    return orders

if __name__ == "__main__":
    # Crear clientes de ejemplo
    print("Aqui haz prubeas mientras no hay buen http")
