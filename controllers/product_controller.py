from fastapi import Depends, HTTPException
from database import get_db
from models.product import Product
import sqlite3

def create_product(product: Product, db: sqlite3.Connection = Depends(get_db)):
    try:
        with db as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO products (name, description, named_has) VALUES (?, ?, ?)",
                           (product.name, product.description, product.named_has))
            db.commit()
            return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_products(db: sqlite3.Connection = Depends(get_db)):
    try:
        with db as db:
            cursor = db.cursor()
            cursor.execute("SELECT id, name, description, named_has, foreing_id FROM products")
            products = cursor.fetchall()
            products = [Product(id=product[0], name=product[1], description=product[2], named_has=product[3], foreing_id=product[4]) for product in products]
            return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
