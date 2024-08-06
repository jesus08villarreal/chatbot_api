from fastapi import APIRouter, Depends
from models.order import Order
from models.order_detail import OrderDetail
from database import get_db
from controllers.order_controller import create_order, create_order_detail
import sqlite3

router = APIRouter()

@router.post("/orders/", response_model=Order)
def create(order: Order, db: sqlite3.Connection = Depends(get_db)):
    return create_order(order, db)

@router.post("/order_details/", response_model=OrderDetail)
def create(order_detail: OrderDetail, db: sqlite3.Connection = Depends(get_db)):
    return create_order_detail(order_detail, db)
