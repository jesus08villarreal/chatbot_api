from fastapi import Depends, HTTPException
from database import get_db
from models.client import Client
import sqlite3

def create_client(client: Client, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO clients (name, phone, email, address, named_has) VALUES (?, ?, ?, ?, ?)",
                   (client.name, client.phone, client.email, client.address, client.named_has))
    db.commit()
    return client

def get_clients(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, phone, email, address, named_has FROM clients")
    clients = cursor.fetchall()
    return clients
