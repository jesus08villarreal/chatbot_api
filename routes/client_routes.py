from fastapi import APIRouter, Depends
from models.client import Client
from typing import List
from database import get_db
from controllers.client_controller import create_client, get_clients, update_client
import sqlite3

router = APIRouter()

@router.post("/clients/", response_model=Client)
def create(client: Client, db: sqlite3.Connection = Depends(get_db)):
    return create_client(client, db)

@router.get("/clients/", response_model=List[Client])
def read_clients(db: sqlite3.Connection = Depends(get_db)):
    return get_clients(db)

@router.put("/clients/{id}", response_model=Client)
def update(id: int, client: Client, db: sqlite3.Connection = Depends(get_db)):
    return update_client(id, client, db)
