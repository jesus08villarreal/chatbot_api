from fastapi import Depends, HTTPException
from database import get_db
from models.order import Order
from models.order_detail import OrderDetail
import sqlite3

def create_order(order: Order, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO orders (client_id, order_date, delivery_date, delivery_time, location, confirmation_status) VALUES (?, ?, ?, ?, ?, ?)",
                   (order.client_id, order.order_date, order.delivery_date, order.delivery_time, order.location, "pending"))
    db.commit()
    return order

def create_order_detail(order_detail: OrderDetail, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO order_details (order_id, product_id, quantity) VALUES (?, ?, ?)",
                   (order_detail.order_id, order_detail.product_id, order_detail.quantity))
    db.commit()
    return order_detail
