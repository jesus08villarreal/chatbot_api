from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.product import Product as ProductModel
import schemas

def create_product(product: schemas.ProductCreate, db: Session):
    with db as db:
        db_product = ProductModel(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

def get_product(db: Session, product_id: int):
    with db as db:
        return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    with db as db:
        return db.query(ProductModel).offset(skip).limit(limit).all()

def update_product(product_id: int, product: schemas.ProductUpdate, db: Session):
    with db as db:
        db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product

def delete_product(product_id: int, db: Session):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}
