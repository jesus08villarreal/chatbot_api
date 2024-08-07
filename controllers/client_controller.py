from fastapi import Depends, HTTPException
from database import get_db
from models.client import Client
import sqlite3

def create_client(client: Client, db: sqlite3.Connection = Depends(get_db)):
    try:
        with db as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO clients (name, phone, email, address, named_has) VALUES (?, ?, ?, ?, ?)",
                           (client.name, client.phone, client.email, client.address, client.named_has))
            db.commit()
            return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_clients(db: sqlite3.Connection = Depends(get_db)):
    try:
        with db as db:  
            cursor = db.cursor()
            cursor.execute("SELECT id, name, phone, email, address, named_has, foreing_id FROM clients")
            clients = cursor.fetchall()
            clients = [Client(id=client[0], name=client[1], phone=client[2], email=client[3], address=client[4], named_has=client[5], foreing_id=client[6]) for client in clients]
            return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_client(id: int, client: Client, db: sqlite3.Connection = Depends(get_db)):
    try:
        with db as db:
            cursor = db.cursor()
            cursor.execute("UPDATE clients SET name = ?, phone = ?, email = ?, address = ?, named_has = ?, foreing_id = ? WHERE id = ?",
                           (client.name, client.phone, client.email, client.address, client.named_has, client.foreing_id, id))
            db.commit()
            return client
            

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))