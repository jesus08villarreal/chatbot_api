import sqlite3

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

if __name__ == "__main__":
    # Crear clientes de ejemplo
    create_client("Carlos Cavazos", "+5218114906600", "carlos.cavazos@gmail.com", "Toribio", "Charlie, Carlos Cavazos, carlos, carlos cavazos", 6)
