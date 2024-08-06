from fastapi import APIRouter, Depends
from models.product import Product
from controllers.product_controller import create_product, get_products
import sqlite3
from typing import List
from database import get_db

router = APIRouter()

@router.post("/products/", response_model=Product)
def create(product: Product, db: sqlite3.Connection = Depends(get_db)):
    return create_product(product, db)

@router.get("/products/", response_model=List[Product])
def read_products(db: sqlite3.Connection = Depends(get_db)):
    return get_products(db)
