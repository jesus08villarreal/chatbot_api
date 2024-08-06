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
    create_client("Juan Pérez", "5551234567", "juan.perez@example.com", "Calle Falsa 123", "juan, perez, jp", 1)
    create_client("María López", "5557654321", "maria.lopez@example.com", "Avenida Siempre Viva 456", "maria, lopez, ml", 2)
    create_client("Carlos Sánchez", "5559876543", "carlos.sanchez@example.com", "Boulevard Central 789", "carlos, sanchez, cs", 3)
    create_client("Ana Fernández", "5556543210", "ana.fernandez@example.com", "Calle Principal 321", "ana, fernandez, af", 4)
    create_client("Luis Ramírez", "5554321098", "luis.ramirez@example.com", "Avenida del Pan 111", "luis, ramirez, lr", 5)

    # Crear productos de ejemplo
    create_product("Baguette", "Pan francés crujiente y alargado.", "baguette, pan francés", 1)
    create_product("Bolillo", "Pan blanco redondo, ideal para tortas.", "bolillo, pan blanco", 2)
    create_product("Concha", "Pan dulce esponjoso con cubierta azucarada.", "concha, pan dulce", 3)
    create_product("Pan de muerto", "Pan dulce tradicional con forma de huesos.", "pan de muerto, pan tradicional", 4)
    create_product("Cuernito", "Pan en forma de media luna, similar al croissant.", "cuernito, croissant", 5)
