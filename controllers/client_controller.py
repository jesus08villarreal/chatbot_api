from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.client import Client as ClientModel
import schemas

def create_client(client: schemas.ClientCreate, db: Session):
    with db as db:
        db_client = ClientModel(**client.model_dump())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

def get_client(db: Session, client_id: int):
    with db as db:
        return db.query(ClientModel).filter(ClientModel.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    with db as db:
        return db.query(ClientModel).offset(skip).limit(limit).all()

def update_client(client_id: int, client: schemas.ClientUpdate, db: Session):
    with db as db:
        db_client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail="Client not found")
        for key, value in client.model_dump().items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
        return db_client

def delete_client(client_id: int, db: Session):
    with db as db:
        db_client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail="Client not found")
        db.delete(db_client)
        db.commit()
        return {"detail": "Client deleted"}
