from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.order import Order as OrderModel
from models.order_detail import OrderDetail as OrderDetailModel
import schemas

def create_order(order: schemas.OrderCreate, db: Session):
    with db as db:
        db_order = OrderModel(**order.model_dump())
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session):
    with db as db:
        db_order_detail = OrderDetailModel(**order_detail.model_dump())
        db.add(db_order_detail)
        db.commit()
        db.refresh(db_order_detail)
        return db_order_detail

def get_order(db: Session, order_id: int):
    with db as db:
        return db.query(OrderModel).filter(OrderModel.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    with db as db:
        return db.query(OrderModel).offset(skip).limit(limit).all()

def update_order(order_id: int, order: schemas.OrderUpdate, db: Session):
    with db as db:
        db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        for key, value in order.model_dump().items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
        return db_order

def delete_order(order_id: int, db: Session):
    with db as db:
        db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        db.delete(db_order)
        db.commit()
        return {"detail": "Order deleted"}
    
def get_order_details(db: Session, order_id: int):
    with db as db:
        return db.query(OrderDetailModel).filter(OrderDetailModel.order_id == order_id).all()
    
def get_orders_by_date(db: Session, date: str):
    with db as db:
        return db.query(OrderModel).filter(OrderModel.delivery_date == date).all()
