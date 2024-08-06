from fastapi import Depends, HTTPException
from database import get_db
from models.product import Product
import sqlite3

def create_product(product: Product, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO products (name, description, named_has) VALUES (?, ?, ?)",
                   (product.name, product.description, product.named_has))
    db.commit()
    return product

def get_products(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, description, named_has FROM products")
    products = cursor.fetchall()
    return products
